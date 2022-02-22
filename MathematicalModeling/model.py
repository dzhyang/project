import tensorflow as tf

class Network:
    def __init__(self):
        # 学习速率，一般在 0.00001 - 0.5 之间
        self.learning_rate = 0.02

        self.x = tf.placeholder(tf.float32, [None, 16],"input")

        self.label = tf.placeholder(tf.float32, [None, 2], "lable")
        
        self.node=10
        #第一层
        # 权重
        self.w_1 = tf.get_variable("W_1",initializer=tf.ones([16, self.node]))
        tf.summary.histogram("one"+'/Weights',self.w_1)
        # 偏置 bias 
        self.b_1 = tf.get_variable("B_1",initializer= tf.zeros([self.node]))        
        tf.summary.histogram("one"+'/biases',self.b_1)
        # 输出 y = tanh(X * w + b)
        self.y_1 = tf.nn.tanh(tf.matmul(self.x, self.w_1) + self.b_1,name="layer_1")
        
        #第二层

        # 权重
        self.w_2 = tf.get_variable("W_2",initializer=tf.ones([self.node, 2]))
        tf.summary.histogram("two"+'/Weights',self.w_2)
        
        # 偏置 bias
        self.b_2 = tf.get_variable("B_2",initializer=tf.zeros([2]))
        tf.summary.histogram("two"+'/biases',self.b_2)

        # 输出 y = softmax(X * w + b)
        self.y_2 = tf.nn.softmax(tf.matmul(self.y_1, self.w_2) + self.b_2,name="layer_2")
    

        # 损失，即交叉熵，最常用的计算标签(label)与输出(y)之间差别的方法
        self.error_loss = -tf.reduce_sum(self.label * tf.log(self.y_2 + 1e-10),name="loss_train")
        tf.summary.scalar('Loss_Image', self.error_loss)
        
        #正则化
        tf.add_to_collection("losses",self.error_loss)              
        regularizer = tf.contrib.layers.l1_regularizer(0.01)
        regularization = regularizer(self.w_1) + regularizer(self.w_2)
        tf.add_to_collection("losses", regularization)
        self.loss=tf.add_n(tf.get_collection("losses"))

        # 反向传播，采用梯度下降的方法。调整w与b，使得损失(loss)最小
        # loss越小，那么计算出来的y值与 标签(label)值越接近，准确率越高
        self.train = tf.train.AdadeltaOptimizer(self.learning_rate).minimize(self.loss)

        
        
        # 以下代码验证正确率时使用
        predict = tf.equal(tf.argmax(self.label,1,name="Get_label"),tf.argmax(self.y_2,1,name="Get_output"))
        
        # reduce_mean即求predict的平均数 即 正确个数 / 总数，即正确率
        self.accuracy = tf.reduce_mean(tf.cast(predict, "float"),name="Accuracy")

        #训练中测试损失值 
        self.test_loss= -tf.reduce_sum(self.label * tf.log(self.y_2 + 1e-10),name="loss_test")
        tf.summary.scalar('Test_Image', self.test_loss)
        
        #测试使用
        self.result=self.y_2
