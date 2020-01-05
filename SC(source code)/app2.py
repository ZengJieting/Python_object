from flask import Flask, render_template, request
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Line, Bar
from flask import Flask, render_template, request
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Line, Bar,Pie
from pyecharts.globals import ThemeType

app = Flask(__name__)

# 地图 读取csv数据  通过逗号分隔  指定编码格式GBK
df_map = pd.read_csv('./csv/map.csv', encoding='GBK', delimiter=",")
# 提取map.csv中region的数据并去重再转化成list
regions_available_map = list(df_map['region'].dropna().unique())

# 折线图
df_line = pd.read_csv('./csv/line.csv', encoding='GBK', delimiter=",")

# 柱状图
df_bar = pd.read_csv('./csv/bar.csv', encoding='GBK', delimiter=",")
regions_available_bar = list(df_bar['region'].dropna().unique())

# base
df_base = pd.read_csv('./csv/acs2.csv', encoding='GBK', delimiter=",")
regions_available_base = list(df_base['region'].dropna().unique())

# develop
df_develop = pd.read_csv('./csv/bar2.csv', encoding='GBK', delimiter=",")
regions_available_develop = list(df_develop['region'].dropna().unique())

# pie
df_pie = pd.read_csv('./csv/pie.csv', encoding='GBK', delimiter=",")
regions_available_pie = list(df_pie['region'].dropna().unique())


# 访问首页  带上mark = index 参数
@app.route('/', methods=['GET'])
def hu_run_2019():
    return render_template('pyecharts.html',
                           mark="index", )

# 访问老年人口地图页面
@app.route('/toMap/oldMan', methods=['GET'])
def to_map_old_man():
    return render_template('pyecharts.html',   # 用于给模板html识别显示哪个from标签
                           mark="map_oldMan",    # 用于给模板html 显示下拉选项
                           the_select_year=["2018", "2017", "2016"],
                           )


@app.route('/toMap/citys', methods=['GET'])
def to_map_citys():
    return render_template('pyecharts.html',
                           mark="map_citys",
                           the_select_year=["2018", "2017", "2016"],
                           )


@app.route('/toLine', methods=['GET'])
def to_line():
    return render_template('pyecharts.html',
                           mark="line",
                           )


@app.route('/toBar', methods=['GET'])
def to_bar():
    return render_template('pyecharts.html',
                           mark="bar",
                           the_select_region=regions_available_bar,
                           )
@app.route('/BASE', methods=['GET'])
def to_base():
    return render_template('pyecharts.html',
                           mark="base",
                           the_select_region=regions_available_base,
                           )

@app.route('/DEVELOP', methods=['GET'])
def to_develop():
    return render_template('pyecharts.html',
                           mark="develop",
                           the_select_region=regions_available_develop,
                           )

@app.route('/PIE', methods=['GET'])
def to_pie():
    return render_template('pyecharts.html',
                           mark="pie",
                           the_select_region=regions_available_pie,
                           )


# 柱状图
@app.route('/bar', methods=['POST'])
def bar_select() -> 'html':
    # 获取用户输入的选项
    the_region = request.form["the_region_selected"]
    # 根据用户输入选项提取 对应数据
    dfs_bar = df_bar.query("region=='{}'".format(the_region))
    # 创建图表对象并配置参数

    c = (
        Bar()
            .add_xaxis(dfs_bar['年'].tolist()) # 配置x轴数据
            .add_yaxis(the_region, dfs_bar['count'].tolist())# 配置y轴数据
            .set_global_opts(title_opts=opts.TitleOpts(title=the_region, subtitle=""))# 配置标题
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
     )
    )
    # 生成图表html文件
    c.render("./static/tmp/echarts_bar.html")
    # 读取生成好的图表
    with open("./static/tmp/echarts_bar.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    # 准备模板显示用的 表格数据
    data_str = dfs_bar.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,# 图表
                           the_res=data_str, # 表格数据
                           the_select_region=regions_available_bar,#下拉框数据
                           bottom_title="随着人口老龄化程度的提高，居民的养老意识也逐渐有所提升，主要体现在城乡居民的参保人数和参保支出的增多，但实际领取待遇的人数不足30%。",# 图表下标题数据
                           mark="bar",# 用于给模板html识别显示柱状图对应的from标签
                           )


# 2018
@app.route('/base', methods=['POST'])
def base_select() -> 'html':
    the_region = request.form["the_region_selected"]
    dfs_base = df_base.query("region=='{}'".format(the_region))

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
            .add_xaxis(dfs_base['地区'].tolist())
            .add_yaxis(the_region, dfs_base['count'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=the_region, subtitle=""),
                             xaxis_opts=opts.AxisOpts(name="地区", axislabel_opts={"rotate": 45}),
                             datazoom_opts=[opts.DataZoomOpts()])
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"), ])
        )
    )

    c.render("./static/tmp/echarts_2018bar.html")
    with open("./static/tmp/echarts_2018bar.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    data_str = dfs_base.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           the_res=data_str,
                           the_select_region=regions_available_base,
                           bottom_title="而在2018年，各省养老院分布较不平均，且规模较小，主要是集中在50-100张床位的数量的规模上。伴随养老意识的普及，需求还将进一步提升，未来养老院行业规模仍将不断扩大。",
                           mark="base",
                           )


# DE
@app.route('/develop', methods=['POST'])
def develop_select() -> 'html':
    the_region = request.form["the_region_selected"]
    dfs_develop = df_develop.query("region=='{}'".format(the_region))

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
            .add_xaxis(dfs_develop['年'].tolist())
            .add_yaxis("", dfs_develop['count'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=the_region, subtitle=""))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )
    )
    c.render("./static/tmp/echarts_develop.html")
    with open("./static/tmp/echarts_develop.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    data_str = dfs_develop.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           the_res=data_str,
                           the_select_region=regions_available_develop,
                           bottom_title="我国人口老龄化问题日渐加剧，老龄人口数量逐年攀升，对养老院的需求趋于旺盛。养老机构数量和床位数不断增加，但从15年开始增长较慢。国内的养老行业却存在较大的供给缺口。",
                           mark="develop",
                           )


# PIE
@app.route('/pie', methods=['POST'])
def pie_select() -> 'html':
    the_region = request.form["the_region_selected"]
    dfs_pie = df_pie.query("region=='{}'".format(the_region))

    c = (
        Pie()
            .add("", [list(z) for z in zip(dfs_pie["地区"], dfs_pie["count"])])
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    c.render("./static/tmp/echarts_pie.html")
    with open("./static/tmp/echarts_pie.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    data_str = dfs_pie.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           the_res=data_str,
                           the_select_region=regions_available_pie,
                           bottom_title="目前养老院行业主要是以国营为主，PPP模式下（公共私营合作制）的养老行业在近年来备受青睐，但也面临着许多问题。养老PPP项目布局严重不平衡，不足以解决多地养老服务设施短缺的问题，且养老PPP回报机制单一化和同质化。未来“PPP+养老”需要社会共同关注和努力。",
                           mark="pie",
                           )


@app.route('/line', methods=['POST'])
def line_select() -> 'html':
    d = {"20162": "2016年人口老龄化程度（%）",
         "20172": "2017年人口老龄化程度（%）",
         "20182": "2018年老年人人口抚养比（%）",
         "2016": "2016年老年人人口抚养比（%）",
         "2017": "2017年老年人人口抚养比（%）",
         "2018": "2018年老年人人口抚养比（%）",
         "2018urual": "2018年农村老年人人口抚养比（%）",
         "2018city": "2018年城市老年人人口抚养比（%）",
         }
    the_region = request.form["the_region_selected"]
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
            .add_xaxis(df_line['地区'].tolist())
            .add_yaxis("", df_line[the_region])
            .set_global_opts(title_opts=opts.TitleOpts(title=d[the_region]),
                             xaxis_opts=opts.AxisOpts(name="地区", axislabel_opts={"rotate": 45}),
                             datazoom_opts=[opts.DataZoomOpts()], )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="最小值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        ))

    c.render("./static/tmp/echarts_line.html")
    with open("./static/tmp/echarts_line.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    data_str = df_line.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           the_res=data_str,
                           mark="line",
                           bottom_title="2018年，人口老龄化程度达11.28%，接近联合国发布的老龄化社会的深度阶段。人口老龄化程度的提高，老年人人口抚养比也随之提高。城市化的背后是农村的年轻人流入了城市，抬高了农村的老龄化程度。",
                           )


# 老年人口地图
@app.route('/map/oldMan', methods=['POST'])
def map_select() -> 'html':
    the_region = regions_available_map[0]
    dfs = df_map.query("region=='{}'".format(the_region))
    the_year = request.form["the_year_selected"]
    chart = (
        Map()
            .add(series_name=the_region, data_pair=[list(z) for z in zip(dfs["地区"], dfs[the_year])], maptype="china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title=the_year + the_region),
            visualmap_opts=opts.VisualMapOpts(max_=10000),
        )
    )
    chart.render("./static/tmp/echarts_map.html")
    with open("./static/tmp/echarts_map.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    data_str = dfs.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           mark="map_oldMan",
                           the_res=data_str,
                           the_select_year=["2018", "2017", "2016"],
                           bottom_title="近三年来，我国老年人人口数量整体呈上升趋势，主要以东部沿海地区往西部地区递减，其中山东、河南、四川老年人口数量最多。",
                           )


# 城市化地图
@app.route('/map/citys', methods=['POST'])
def map_select_citys() -> 'html':
    the_region = regions_available_map[1]
    dfs = df_map.query("region=='{}'".format(the_region))
    the_year = request.form["the_year_selected"]

    # 切掉百分号
    ndfs = dfs[the_year].apply(lambda x: x[0:5]).astype('float')

    chart = (
        Map()
            .add(series_name=the_region, data_pair=[list(z) for z in zip(dfs["地区"], ndfs)], maptype="china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title=the_year + the_region),
            visualmap_opts=opts.VisualMapOpts(min_=28, max_=90),
        )
    )
    chart.render("./static/tmp/echarts_map.html")
    with open("./static/tmp/echarts_map.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    data_str = dfs.to_html()
    return render_template('pyecharts.html',
                           myechart=plot_all,
                           mark="map_citys",
                           the_res=data_str,
                           the_select_year=["2018", "2017", "2016"],
                           bottom_title="城市化最早的地区的老龄化相对严重，例如京津沪三个直辖市、东三省。这些地区在计划经济时期中的国有经济占比高、历史长，职工依赖于单位，也是执行计划生育最彻底、最严格的地区，这进一步提升了老龄化的程度。",
                           )


if __name__ == '__main__':
    app.run(debug=True, port=8083)
