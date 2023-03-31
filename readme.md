# 背景介绍

~~可泛化为多个场景的批量算路算法~~

堵路系统。。。

# 条件约束

- ~~图的表示：邻接矩阵（numpy）~~
- 主体的表示：图中的个体，可以体现泛化性（个体可以指taxi，交警，等等）

# 算法

- dijstra
- A*
- 矩阵乘法

# workFlow

- 先把地图弄出来，以北京为例
- 然后使用h3库进行六边形分割
- 然后找数据进行训练
- 训练后可视化

# 数据集

- 微软数据集：

https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/

# GPT suggestion

你的项目“重点人员轨迹预测与控制系统”在实际中具有以下应用方面的亮点：

1. 安全防控方面：你的项目可以通过对重点人员轨迹进行预测和控制，为公共安全防控提供技术支撑。例如，当有疑似犯罪嫌疑人出现在某个区域时，该系统可以及时预测其下一步行动，提前制定应对策略，从而避免可能的安全风险。
2. 执法监管方面：你的项目可以为执法部门提供技术支撑，帮助其更好地监管和管控重点人员的行动。例如，该系统可以对监管区域内的重点人员进行实时轨迹监控，提供预测和控制服务，从而提高执法部门的工作效率和监管水平。
3. 城市规划方面：你的项目可以对城市规划和管理提供参考意见。例如，该系统可以对重点人员的活动范围和行为规律进行分析和展示，帮助城市规划者更好地了解城市人口流动特征和行为习惯，从而优化城市规划和管理。
4. 商业分析方面：你的项目可以对商业活动和市场营销进行分析。例如，该系统可以对商业区域内的重点人员进行实时轨迹监控和行为分析，帮助商家更好地了解消费者的需求和行为特征，从而制定更有效的营销策略。

总之，你的项目在公共安全防控、执法监管、城市规划和商业分析等方面都具有较大的应用价值，有望为社会治理和经济发展带来积极的贡献。

以下是一些实际生活中发生过的案例，这些案例可以支撑项目在安全防控方面的应用：

1. 2017年10月31日，美国纽约曼哈顿发生一起恐怖袭击事件，造成8人死亡。该事件发生后，警方利用视频监控及相关技术对肇事者的行踪进行追踪和预测，最终将其抓捕。如果在事件发生前，类似于你的“重点人员轨迹预测与控制系统”能够及时预测和掌握肇事者的行踪，或许这起事件的后果可以被避免或减轻。
2. 2016年3月22日，比利时布鲁塞尔机场和地铁发生恐怖袭击事件，造成多人死亡。如果当时有类似于你的“重点人员轨迹预测与控制系统”，就可以对附近区域的重点人员进行实时监控和预测，帮助相关部门及时发现和处置潜在安全隐患。
3. 在中国，2014年北京西站发生了一起恐怖袭击事件，导致三人死亡和多人受伤。如果类似于你的“重点人员轨迹预测与控制系统”能够及时预测和掌握事件的可能性，并且对重点人员进行实时监控和预测，或许这起事件的后果可以被避免或减轻。

综上所述，类似于你的“重点人员轨迹预测与控制系统”在安全防控方面的应用具有重要的意义和价值。通过对重点人员轨迹的实时监控和预测，可以帮助相关部门及时发现和处置潜在安全隐患，提高社会治安水平。

## 基于GPT suggestion 的update

本项目提供如下功能：

- 对于输入轨迹，计算轨迹异常度
- 对于确认异常的轨迹，在预测的基础上给出拦截方案
