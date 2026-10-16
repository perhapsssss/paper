# 术语表

| English term | Chinese rendering | Policy | Explanation | First seen |
|---|---|---|---|---|
| domain randomization (DR) | 域随机化（domain randomization） | translate-with-English | 在训练时随机改变仿真环境参数，以提升策略对环境变化的适应能力。 | 摘要 |
| reality gap | 现实差距（reality gap） | translate-with-English | 仿真环境与真实物理系统之间的差异。 | 1 |
| Domain Randomization Off-Policy Optimization (DROPO) | 离线策略域随机化优化（DROPO） | keep-English-first | 利用预先采集的离线轨迹，通过似然目标拟合动力学参数分布的方法。 | 摘要 |
| dynamics parameter distribution | 动力学参数分布 | translate | 表示仿真物理参数变化及其不确定性的概率分布。 | 摘要 |
| off-policy data | 离策略数据（off-policy data） | translate-with-English | 由非当前待训练策略采集的数据，也包括人类示范。 | 摘要 |
| likelihood | 似然（likelihood） | translate-with-English | 在给定模型及参数分布时，观测到数据的概率密度。 | 1 |
| unmodeled phenomenon | 未建模现象（unmodeled phenomenon） | translate-with-English | 真实系统中存在但仿真器未显式描述的效应。 | 摘要 |
| point-estimate dynamics | 点估计动力学（point-estimate dynamics） | translate-with-English | 将每个动力学参数视为单一确定值，而非随机分布。 | 2 |
| heteroscedasticity | 异方差（heteroscedasticity） | translate-with-English | 数据的不确定性或噪声方差随条件变化的现象。 | 3.4 |
| CMA-ES | 协方差矩阵自适应进化策略（CMA-ES） | keep-English | 一种无梯度的随机优化算法。 | 3.4 |
| Akima spline | Akima 样条 | translate-with-English | 用于平滑插值的分段样条方法，能减少区间内过冲。 | 3.3 |
| zero-shot transfer | 零样本迁移（zero-shot transfer） | translate-with-English | 未在目标真实系统上额外训练或微调，直接部署策略。 | 4 |
| kinesthetic teaching | 动觉示教（kinesthetic teaching） | translate-with-English | 人通过直接带动机器人完成动作来提供示范。 | 4.3.2 |
| VAE | 变分自编码器（VAE） | translate-with-English | 用于学习低维潜在表示及其解码生成器的概率模型。 | 4.3.1 |
| PPO | 近端策略优化（PPO） | translate-with-English | 一种策略梯度强化学习算法。 | 3.5 |
| SAC | 软演员—评论家（SAC） | translate-with-English | 一种基于最大熵目标的离策略强化学习算法。 | 3.5 |
