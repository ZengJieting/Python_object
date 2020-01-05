# 项目概况（project overview）：

***

### 项目主题（topic）：我国近年人口老龄化与养老行业情况分析

***

### 项目相关（correlation）

* 项目代码 GitHub_URL：[请点击这里](https://github.com/ZengJieting/Python_object/tree/master/SC(source%20code))

* pythonanywhere的个人部署URL：[请点击这里](http://zengjieting.pythonanywhere.com/)

***

### 个人网站介绍（website）

#### 数据源一共有6个（acs2.csv、bar.csv、bar2.csv、line.csv、map.csv、pie.csv）

#### 所呈现的网页URL一共有8个，其中一共7份图表

* [网站首页](http://zengjieting.pythonanywhere.com/)

* [各省老年人人口数量](http://zengjieting.pythonanywhere.com/toMap/oldMan)

* [各省城市化率](http://zengjieting.pythonanywhere.com/toMap/citys)

* [老年人人口抚养比](http://zengjieting.pythonanywhere.com/toLine)

* [近五年养老保险情况分析](http://zengjieting.pythonanywhere.com/toBar)

* [近五年养老院发展趋势](http://zengjieting.pythonanywhere.com/DEVELOP)

* [2018年养老院行业情况](http://zengjieting.pythonanywhere.com/BASE)

* [PPP模式下的养老行业](http://zengjieting.pythonanywhere.com/PIE)

***

### 项目合作者（cooperator）：

* 中山大学南方学院网络与新媒体专业2017级：杨幸（171013089）

* 中山大学南方学院网络与新媒体专业2018级：曾洁婷（181013024）、谭天冠（181013089）

***

### 项目主要内容（content）

* 利用17级师姐杨幸提供的数据以及产出的交互式数据可视化产品，18级处理成可交互的网页，其中含有一些交互控件的功能实现以及数据的传递过滤，同时也实现了不同HTML的相互交互。

***

### 我主要负责的内容

* 后四个数据的传递。（近五年养老保险情况分析、近五年养老院发展趋势、2018年养老院行业情况、PPP模式下的养老行业）

* 页面轮播图与侧边栏组件的插入（轮播图为18级两人共同协作）

***

# 数据传递描述（data transfer description）

***

### HTML档描述

1. 整体页面布局

* **text-align: center;** 定义整体文字元素居中布局，这样也使页面不过分杂乱；**background: papayawhip;** 定义页面的背景颜色。

* <style>中定义分页面的按钮样式：hover、active、visited、focus等动作应用各种效果，具体查看源代码。

2. 交互组件的添加

* 轮播图：轮播图中通过href标签的设置，达成图片与外网链接之间的相互连接。

* 侧边工具栏：分别链接了项目的仓库地址以及三位组员的GitHub页面，同时，最后一个按钮可以在页面下拉的时候迅速回到顶部。

* 页面按钮：每一个按钮都是一个页面的链接，通过href字段链接到每一个主题图表的主页；此外增加了悬停变色、点击会下陷等按钮效果。

* 下拉框的设置：通过下拉可以选择想要了解的数据类型，然后用户选择的数据就会被过滤出来，在后台转换成交互式数据可视化图表。

3. 数据结构

* {% if mark == "line" %}：如果参数mark == line的时候 显示柱状图对应的下拉框，之后“input”执行“do it”命令，提交用户选择数据。{% if mark == "bar" %}、{% if mark == "base" %}、{% if mark == "develop" %}、{% if mark == "pie" %}、{% if mark == "map_oldMan" %}、{% if mark == "map_citys" %} 同理，都是为了方便对提交的数据有一个识别功能，之后更好地对数据进行分析与转化，实现对各种数据的提取。

4. 与python档的交互

* {{ myechart|safe }}、{{ bottom_title|safe }}、{{ the_res|safe }}，在HTML档，有这样的几个空的图标容器，分别用来“装”用户所选择的数据转化出来的可视化产品。{{ myechart|safe }}显示图表，{{ bottom_title|safe }}显示图表下标题，{{ the_res|safe }}显示表格数据。只有当用户选择了，才会有数据的传递，之后通过后端py文件对数据的过滤、筛选和传输，把用户选择的数据“丢进”这样的容器中，图表和相关数据就可以显示出来了。

***

### python档描述

* 主要引用的模块有flask、pandas、pyecharts。

* 数据的读取：如df_map = pd.read_csv('./csv/map.csv', encoding='GBK', delimiter=",") 表示的是读取了csv数据，并且通过逗号分隔，指定编码格式是GBK。

* 数据的提取与转化：如regions_available_map = list(df_map['region'].dropna().unique()) 就是提取map.csv中region的数据并去重再转化成list。

* 用@app.route（路由规则）的方式绑定视图函数，route()告诉Flask 什么样的URL才能触发我们的函数，之后读取数据才能转换成相对应的图表。

* 举一个例子：def bar_select() -> 'html':获取用户输入的选项；the_region = request.form["the_region_selected"]是根据用户输入选项提取对应数据；dfs_bar = df_bar.query("region=='{}'".format(the_region))就最终创建图标对象并配置参数。

***

### webapp动作描述

* 选择按钮：项目启动后，页面会有不同数据主题的七个按钮，每一个按钮点击之后都会跳转到相对应的数据选择页面，并可以通过数据类型选择生成图表，显示相对应的数据分析故事。

* 下拉框：下拉框可以选择不同的数据类型，通过下拉动作并执行“do it”就可以生成所选数据对应的图表页面。

* 轮播图点击：主页面有一个自动播放的轮播图，每一张图片点击可以跳转到相关页面的文章内容。

* 右侧工具栏点击：通过不同选择可以跳转到项目仓库地址或是成员们的GitHub地址，最下面的按钮能够快速回到页面顶部。
