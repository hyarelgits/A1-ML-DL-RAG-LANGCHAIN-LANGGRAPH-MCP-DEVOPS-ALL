# Step 4 - AI Training - 3 Models Together
# 1. Supervised - LogisticRegression - Learns from X and y
# 2. Unsupervised - KMeans - Learns from X only, makes groups
# 3. Deep Learning - MLPClassifier - Neural Network, hidden layer

from sklearn.linear_model import LogisticRegression
# # sklearn = AI library, linear_model = Linear models, LogisticRegression = For Yes/No prediction
from sklearn.cluster import KMeans
# # cluster = Clustering, KMeans = Make groups/clusters
from sklearn.neural_network import MLPClassifier
# # neural_network = Neural Network, MLPClassifier = Multi-Layer Perceptron - Deep Learning
import pickle
# # pickle = Save model to file, like saving knowledge in notebook
import os
# # os = To get file path

X = [[750], [680], [550], [720], [600], [800]]
# # X = Input, List of lists, each inner list is one sample - Risk Score
# # 750 = High risk, 550 = Low risk - Example numbers
y = [1, 1, 0, 1, 0, 1]
# # y = Answer, 1 = malware, 0 = normal - Same order as X
# # X[0]=750 -> y[0]=1, X[2]=550 -> y[2]=0, etc.

print("Training Started...")
# # print = Show message

print("1. Supervised - LogisticRegression")
# # Print heading for Supervised
sup = LogisticRegression()
# # sup = Object of LogisticRegression, sup = Supervised model
sup.fit(X, y)
# # fit(X, y) = Learn from Input X and Answer y - Like Father teaches Kid with Q + A
print("Supervised Predict for 700:", sup.predict([[700]]))
# # predict([[700]]) = Guess for new input 700, [[700]] = List of list, because model expects 2D
# # Expected: [1] = malware

print("2. Unsupervised - KMeans")
# # Print heading for Unsupervised
unsup = KMeans(n_clusters=2, random_state=42, n_init=10)
# # unsup = KMeans object, n_clusters=2 = Make 2 groups, random_state=42 = Same result every time, n_init=10 = Try 10 times
unsup.fit(X)
# # fit(X) = Learn from X only, NO y - Like Teacher gives only Q, no A, Kid makes groups himself
print("KMeans Clusters for our 6 data:", unsup.labels_)
# # labels_ = Which group each X belongs to - Example [1 1 0 1 0 1]
print("KMeans Predict for 700 - Which Group:", unsup.predict([[700]]))
# # predict([[700]]) = Which group does 700 belong to? 0 or 1

print("3. Deep Learning - MLPClassifier")
# # Print heading for Deep Learning
dl = MLPClassifier(hidden_layer_sizes=(10,), max_iter=500, random_state=42)
# # dl = Deep Learning model, hidden_layer_sizes=(10,) = 10 neurons in hidden layer - Brain inside
# # max_iter=500 = Train max 500 times, random_state=42 = Same result every time
dl.fit(X, y)
# # fit(X, y) = Learn from X and y, but with neural network - Input -> Hidden (10) -> Output
print("DL Predict for 700:", dl.predict([[700]]))
# # predict = Guess for 700 - Expected [1]

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
# # model_path = backend/model.pkl - Where to save model
pickle.dump(sup, open(model_path, "wb"))
# # pickle.dump(sup, ...) = Save sup model to file, "wb" = Write Binary
print("Model saved to:", model_path)
# # Print where model saved
print("Training Done - All 3 Models Working")
# # Print done
