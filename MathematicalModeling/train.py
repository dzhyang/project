#引入依赖库
import tensorflow as tf
import xlrd
import random
from sklearn import preprocessing  

#定义神经网络模型
class Network:
    def __init__(self):
        # 学习速率，一般在 0.00001 - 0.5 之间
        self.learning_rate = 0.02

        self.x = tf.placeholder(tf.float32, [None, 16],"input")

        self.label = tf.placeholder(tf.float32, [None, 2], "lable")
        
        self.node = 10
        
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



#定义训练及数据处理方法类
class Train:
    def __init__(self):
        self.net = Network()
        self.saver=tf.train.Saver()
        # 初始化 session
        # Network() 只是构造了一张计算图，计算需要放到会话(session)中
        self.sess = tf.Session()
        # 初始化变量
        self.sess.run(tf.global_variables_initializer())

        # 读取训练和测试数据
        book = xlrd.open_workbook("./数字化处理文件.xlsx")
        self.ReadMatrix_Input = []
        self.ReadMatrix_Output=[]
        sheet = book.sheet_by_index(0)
        for i in range(0, 65535):
            temporary_In = []
            for j in range(1, sheet.ncols - 3):
                temporary_In.append(sheet.row_values(i)[j])
            
            if sheet.row_values(i)[sheet.ncols - 3]==1:                
                self.ReadMatrix_Output.append([0, 1])#续保
            else:
                self.ReadMatrix_Output.append([1, 0])#不续保         
            self.ReadMatrix_Input.append(temporary_In)
        
        #输入数据归一化，减少差距
        PM = preprocessing.MinMaxScaler()
        self.Input_x = PM.fit_transform(self.ReadMatrix_Input)
        
        #模型读取
        Path=tf.train.get_checkpoint_state("./Model_Save")
        if Path and Path.model_checkpoint_path:
            self.saver.restore(self.sess, Path.model_checkpoint_path)
        else:
            self.train()
        
    #获取训练集的训练数据
    def Get_traing(self,parameter_list):
        _x = []
        _label=[]
        for target_list in range(0, parameter_list):
            l = random.randint(0, 50000)
            _x.append(self.Input_x[l])
            _label.append(self.ReadMatrix_Output[l])
        return _x,_label
    #获取测试集的测试数据
    def Get_test(self,parameter_list):
        _x = []
        _label=[]
        for target_list in range(0, parameter_list):
            l = random.randint(50001, 65534)
            _x.append(self.Input_x[l])
            _label.append(self.ReadMatrix_Output[l])
        return _x,_label

    #训练
    def train(self):
        # batch_size 是指每次迭代训练，传入训练的数据数量。
        batch_size = 64
        # 总的训练次数
        train_step = 70000
        #计算结果可视化
        merged=tf.summary.merge_all()
        write=tf.summary.FileWriter("./logs/", self.sess.graph)
        # 开始训练
        for i in range(train_step):
            # 从数据集中获取 输入和标签(也就是答案)
            x, label = self.Get_traing(batch_size)
            # 每次计算train，更新整个网络
            # loss只是为了看到损失的大小，方便打印
            _, loss_1,rs = self.sess.run([self.net.train, self.net.loss,merged],
                                    feed_dict={self.net.x:x, self.net.label:label})
            write.add_summary(rs, i)

            #计算测试损失值
            x_t, label_t = self.Get_test(batch_size)
            test_loss,m = self.sess.run([self.net.test_loss,merged],
                                 feed_dict={self.net.x: x_t, self.net.label: label_t})
            write.add_summary(m, i)
            # 打印 loss，训练过程中将会看到，loss有变小的趋势   
            # 但是由于网络规模较小，后期没有明显下降，而是有明显波动
            if (i + 1) % 1000== 0:
                print('第%5d步，当前train_loss：%.5f' % (i + 1, loss_1))
                print('第%5d步，当前test_loss：%.5f \n' % (i + 1, test_loss))
                
        #训练后的模型存储
        self.saver.save(self.sess,"./Model_Save/defult")
    
    #测试模型准确率
    def calculate_accuracy(self):
        
        x_t, label_t = self.Get_test(1)
        # 注意：与训练不同的是，并没有计算 self.net.train
        # 只计算了accuracy这个张量，所以不会更新网络
        
        accuracy,w_1,b_1,w_2,b_2 = self.sess.run([self.net.accuracy,self.net.w_1,self.net.b_1,self.net.w_2,self.net.b_2],
                                 feed_dict={self.net.x: x_t, self.net.label: label_t})
        print(w_1)                         
        print(w_2)                         
        print(b_1)                         
        print(b_2)                         
        print("模型准确率为: %.2f%%" % (accuracy*100))

    #从测试集中选取数据测试
    def predict(self,num):
        for i in range(0, num):
            x_r, label_r = self.Get_test(1)
            
            Out=self.sess.run(self.net.result,feed_dict={self.net.x:x_r})
            
            print("第%d次测试,续保概率为：%.4f%%" % (i + 1, Out[0][1]*100))
            if label_r[0][1]==1:
                print("原始输出为：续保\n")
            else:
                print("原始输出为：不续保\n")

if __name__ == "__main__":
    app = Train()
    app.calculate_accuracy()
    #选取测试集数据测试
    app.predict(10)
    