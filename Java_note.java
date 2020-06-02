Java 随手记录

*********************************************************************
一个.java文件只能包含一个public类，但可以包含多个非public类。
如果有public类，文件名必须和public类的名字相同
java入口程序规定的方法必须是静态方法，方法名必须为main，括号内的参数必须是String数组
一个.java文件是可以有多个方法名为main的函数，但是优先运行public static void main(String args[])
*********************************************************************
1 基本数据类型, 即CPU可以直接进行运算的类型,内存中存的是数值本身。
1.1 整数类型：byte，short，int，long
1.2 浮点数类型：float，double
1.3 字符类型：char。 Java在内存中总是使用Unicode表示字符，所以，一个英文字符和一个中文字符都用一个char类型表示，它们都占用两个字节
1.4 布尔类型：boolean

2 引用类型,引用类型变量在内存放的是数据的引用，即数据的地址，并不是数据本身，引用类型变量是以间接方式去获取数据。属于对象类型。
2.1 字符串类型
2.2 数组
2.3 类 (class)
2.4 接口 (interface)

引用的概念，如果一个变量的类型是 类类型，而非基本类型，那么该变量又叫做引用
new hero() 代表创建了一个hero对象，但仅创建对象无法访问。
为了访问会使用"引用"来代表这个对象， Hero h = new Hero();
h这个变量是Hero类型，又叫做引用，=指 h这个引用来代表这个对象，“代表”在面向对象里，又叫“指向”

*********************************************************************
Java的String和char在内存中总是以Unicode编码表示
*********************************************************************
可变参数用类型...定义，可变参数相当于数组类型
*********************************************************************
字面值, 即给基本类型的变量赋值的方式
*********************************************************************
静态属性，又叫类属性
当一个属性被static修饰的时候，就叫做类属性，又叫做静态属性
当一个属性被声明成类属性，那么所有的对象，都共享一个值

*如果一个属性，每个对象都不一样，比如name，这样的属性就该被设计为对象属性，因为它是跟着对象走的。
*如果一个属性，所有对象都共享，都是一样的，那么就该被设计成类属性

静态方法，又叫类方法
访问一个对象方法，必须建立在有一个对象的前提的基础上
访问类方法，不需要对象的存在，直接就访问

如果在某个方法里，调用了对象属性，这个方法就必须设计为对象方法
如果一个方法，没有调用任何对象属性，那么就可以考虑设计为类方法
*********************************************************************
参考《Java编程思想》 7.1 多形性

类的多态特性, 主要是靠继承和方法覆写来实现。 静态语言Java中需要严格遵守继承，动态语言Python则不用。

常见用法: 给一个方法传一个形参，此形参为父类，但调用时传子类对象，JAVA可自动实现动态绑定。
传父类，调子类，实现子类功能

举例:
//父类 Instrument 有一个play()方法
class Instrument { public void play() {输出("乐器演奏")}; }

//子类 Piano 继承父类，并覆写play()方法
class Piano extends Instrument { public void play() {输出("钢琴演奏")}; }


public class Music {

	//乐器演奏 为静态方法，可直接调用，传入一个形参，为父类Instrument，i为父类引用
	public static void tune(Instrument i) { i.play(); }

	//主程调用
	public static void main(String[] args) {
		//实例化一个子类Piano对象 flute
		Piano flute = new Piano();
		//调用时传子类对象
		tune(flute);
		//运行结果："钢琴演奏"

		//这就是向上转型
		Instrument it = new Piano();
	}

}
 
要实现类的多态，需要如下条件：
1) 父类(接口)引用指向子类对象
2) 调用的方法有重写 
*********************************************************************
方法重写
子类可以继承父类的方法，在继承后，重复提供该方法(方法同名)，就叫做方法的重写，又叫覆盖override
*********************************************************************
方法重载
指方法名一样，但参数类型不一样
*********************************************************************
final关键字
1 final修饰的类，该类不能被继承
2 final修饰的方法，该方法不能被子类重写
3 final修饰的基本类型变量，该变量只有一次赋值的机会。1、直接赋值 2、全部在构造方法中赋初值。
4 final修饰的引用，该引用只有一次指向对象的机会
5 常量，即可公开直接访问，不会变化的值，public static final int pai = 3.1415926 
*********************************************************************
开闭原则: 对扩展开放，对修改封闭
*********************************************************************
super 关键字 参考《廖雪峰教程》 继承
子类不会继承父类的任何构造方法。子类默认的构造方法是编译器自动生成的。
super() 用于调用父类的构造器，里面加参数用于帮助编译器定位到对应的构造器。

当父类存在带参的构造函数，又未写无参构造函数时，则子类的构造函数中必须使用 super()
*********************************************************************
==，用于判断两个引用，是否指向了同一个对象
*********************************************************************
接口(interface) 参考《Java编程思想》 7.5 接口
接口这样描述自己:"对于实现我的所有类，看起来都应该向我现在这个样子"，因此，采用了一个特定接口
的所有代码都知道对于那个接口可能会调用什么方法。这便是接口的全部含义。我们常把接口用于建立类和类
之间的一个"协议"。

为创建一个接口，使用interface关键字。
为生成与一个特定的接口相符的类，要使用implements(实现)关键字。我们要表达的意思是:
"接口看起来就像这个样子，这儿是它具体的工作细节。"

还可以利用继承技术，为一个接口添加新的方法声明，也可将几个接口合并成一个新接口。
*********************************************************************
抽象类
在类中声明一个方法，这个方法没有实现体，是一个空方法。这样的方法叫抽象方法，使用修饰符"abstract"
当一个类有抽象方法时，该类必须被声明为抽象类。

特点：
1 一个类一旦被声明为抽象类，则只可被继承，不能直接实例化
2 一个类中包含了一个或多个抽象方法，类就必须指定成 abstract, 否则报错。如果不包含任何抽象方法，也可以声明为抽象类。

作用:
为子类做一个基本形式，使得能定义在所有子类中通用的一些东西。参考参考《Java编程思想》 7.4 抽象类和方法

与接口的区别：
区别1
1.1 子类只能继承一个抽象类，不能继承多个
1.2 子类可以实现多个接口，即可以 implements a1, a2...an

区别2
2.1 抽象类可以定义，public,protected,package,private
	静态和非静态属性，final和非final属性
2.2 接口中声明的属性，只能是 public static final 的，即便没有显示声明，是默认的。
*********************************************************************
类型转换
规则：从小到大自动转，从大到小强制转
byte b = 5;
int i1 = 10;
b = (byte) i1; 强制转型
*********************************************************************
1 类和类之间的关系

1.1 自身：类自己
1.2 同包子类：处于同一个package的子类
1.3 不同包子类： 处于不同package的子类
1.4 同包类： 处于同一个包，但没有继承关系
1.5 其他类： 在不同包，也没有继承关系

--------------------------------------
|			|  继承关系	 | 非继承关系 |
|------------------------------------|
|	同包		|  同包子类	 | 同包类	 |
|------------------------------------|
|	不同包	|  不同包子类 | 其他类	 |
--------------------------------------


2 成员变量有四种修饰符

2.1 private 私有的
	自身：可以访问
--------------------------------------
|			|  子类  	 |  非子类	 |
|------------------------------------|
|	同包		|  不能继承	 |  不能访问	 |
|------------------------------------|
|	不同包	|  不能继承	 |  不能访问	 |
--------------------------------------

2.2 protected 受保护的
	自身：可以访问
--------------------------------------
|			|  子类  	 |  非子类	 |
|------------------------------------|
|	同包		|  可继承	 |  可访问	 |
|------------------------------------|
|	不同包	|  可继承	 |  不能访问	 |
--------------------------------------

2.3 package/friendly/default 即不写修饰符
	自身：可以访问
--------------------------------------
|			|  子类  	 |  非子类	 |
|------------------------------------|
|	同包		|  可继承	 |  可访问	 |
|------------------------------------|
|	不同包	|  不能继承	 |  不能访问	 |
--------------------------------------

2.4 public 公共的
	自身：可以访问
--------------------------------------
|			|  子类  	 |  非子类	 |
|------------------------------------|
|	同包		|  可继承	 |  可访问	 |
|------------------------------------|
|	不同包	|  可继承	 |  可访问	 |
--------------------------------------

*********************************************************************
I/O

对象流指的是，可以直接把一个对象以流的形式 传输给其他的介质，比如硬盘。
一个对象以流的形式进行传输，叫做序列化。该对象所对应的类，必须是实现Serializable接口。

流
当不同的介质之间有数据交互的时候，Java就使用流来实现。
数据源可以是文件，还可以是数据库，网络甚至是其他的程序。

比如读取文件的数据到程序中，站在程序的角度来看，就叫做输入流
字节输入流：InputStream
字节输出流：OutputStream
用于以字节形式读取和写入数据


