import pandas as pd 
import matplotlib.pyplot as plt
import os


path = "C:./Graphs/conv2d_history.csv"
history = pd.read_csv(path)
df = pd.DataFrame(history)


#displays accuracy and loss
def loss_acc_graph(dataframe):
    df = dataframe
    ax = plt.gca()
    df.plot(kind='line',y = 'accuracy',ax=ax,color='blue')
    df.plot(kind='line',y = 'loss',ax=ax,color='red')

    ax.set_xlabel("Index Values")
    ax.set_ylabel("Latitude Values")
    plt.title('Accuracy & Loss Graph')
    plt.show()
    
#displays validation accuracy and validation loss
def val_graph(dataframe):
    df = dataframe
    ax = plt.gca()
    df.plot(kind='line',y = 'val_accuracy',ax=ax,color='cyan')
    df.plot(kind='line',y = 'val_loss',ax=ax,color='magenta')
    ax.set_xlabel("Index Values")
    ax.set_ylabel("Latitude Values")
    plt.title('Validation Performance Graph')
    plt.show()

#combines both graphs
def main():
    loss_acc_graph(df)
    val_graph(df)

if __name__ == "__main__":
    main()
