import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import numpy as np
from keras import Sequential
from keras._tf_keras.keras.layers import Dense,LSTM
from keras._tf_keras.keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score


actions = np.array(['open', 'close', 'left', 'right'])
label_map = {label:num for num,label in enumerate(actions)}

DATA_PATH = os.path.join('MP_Data')
sequences, labels = [],[]
no_sequences = 30
sequence_length = 30
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH,action,str(sequence),"{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.05,random_state=42)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(64,return_sequences=True,activation='relu', input_shape=(30,1662)))
model.add(LSTM(128,return_sequences=True,activation='relu'))
model.add(LSTM(64,return_sequences=False,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(actions.shape[0],activation='softmax'))

model.compile(optimizer='Adam',loss ='categorical_crossentropy',metrics=['categorical_accuracy'])
model.fit(X_train,y_train,epochs=2000,callbacks=[tb_callback])


res = model.predict(X_test)
# print(res)
# print(np.argmax(res[3]))
# print(actions[np.argmax(res[3])])
# print(actions[np.argmax(y_test[3])])

model.save('action.keras')
