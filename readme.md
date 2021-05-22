# Pyopengl-demo

As is known to programmers, it is relatively tedious and labourious to write codes on Computer Graphics. For exemple, it may take hundreds of lines of C++ codes to generate VBO, VAO, shader, BEFORE a single triangle can be rendered. Combined with the complicated OpenGL API, things become even worse.

That's why I've decided to code the main functionality of Computer Graphics into Python as a practice. *The advanced feature provided by python and numerous handy libs(numpy, etc) can greatly reduce the trivial but tedious parts of coding, and help we programmers **focus on the core logic of computer graphics.***

So far, I've implemented 6 stages of codes, each containing a basic but key feature in computer graphics. The six feature is directly in the root directory, not wrapped into folders yet.

The part below illustrate the first five stages.

***

### Stage 1

源代码取自[一份写给python程序员的opengl教程](https://blog.csdn.net/weixin_42625143/article/details/99721626)

修改了代码，成功封装到了```app.py: class Application```中

### Stage 2

根据[LearnOpenGL-CN-你好，三角形](https://learnopengl-cn.github.io/01%20Getting%20started/04%20Hello%20Triangle/)教程

应用了VAO，VBO，改用shader进行渲染，并封装到了python类中

> 采用numpy传递数据。gl接口中原本填sizeof(data)的地方改为arr.nbytes即可
>
> 用RenderData封装VAO和VBO，没有封装EBO
>
> 智能识别顶点格式，shader智能传递uniform

see: ```shader.py, render_data.py, vert.glsl, frag.glsl```

### Stage 3

加入了纹理，并封装入```texture.py: class Texture```中。

+ 现在会渲染两个纹理混合的一个立方体

纹理图像的加载采用pillow库，见```import PIL```

将变换、摄像机相关代码抽离出来，封装成了```camera.py: class Camera```并优化了代码逻辑，便于日后修改摄像机模式

会绘制xyz轴了

### Stage 4

使用```DearPyGui```包添加了异步（多线程）的gui，解决了一些多线程的问题

+ 现在只有一个选项
+ 但基础框架已经建立了

### Stage 5

完成了phong光照模型，并配上了可以动态修改参数的gui