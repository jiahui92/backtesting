# 启动
* 安装backtesting
* python test.py
  * 依赖包包太旧/新的报错: python3 -m pip install bokeh==2.4.3

# 资料
* [backtesting文档](https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0)
* [量化交易相关资料](https://github.com/wangzhe3224/awesome-systematic-trading/blob/master/Readme_cn.md)
* numpy
* pandas

# 结论
* 趋势投资中比较简单易用的指标，经回测验证能提高盈利
  * MA均线 / MACD
  * BOOL

## MA
* MA5上涨，MA10下跌：短期趋势反转为上涨
* MA5上涨，MA10上涨：短期趋势更好或过热
* MA5下跌，MA10上涨：短期趋势反转为下跌
* MA5下跌，MA10下跌：短期趋势更坏或崩盘
