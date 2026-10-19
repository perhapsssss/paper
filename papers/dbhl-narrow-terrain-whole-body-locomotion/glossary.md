# 术语表

| English term | 中文译法 | Policy | Explanation | 首次出现 |
|---|---|---|---|---|
| Dynamic Balanced Humanoid Locomotion (DBHL) | 动态平衡人形运动（DBHL） | translate-with-English | 本文提出的全身强化学习运动框架。 | 摘要 |
| zero moment point (ZMP) | 零力矩点（ZMP） | translate-with-English | 惯性力与重力合力矩在水平轴方向分量为零的点。 | 摘要 |
| zero moment line (ZML) | 零力矩线（ZML） | translate-with-English | 非平面接触条件下，不同高度处 ZMP 位置组成的轨迹。 | 引言 |
| proprioception | 本体感知 | translate-with-English | 来自机器人自身关节、惯性和接触状态的感知信息。 | 摘要 |
| whole-body control (WBC) | 全身控制（WBC） | translate-with-English | 联合协调多个身体部位和自由度的控制方法。 | II-A |
| asymmetric actor-critic | 非对称 actor-critic | keep-English-first | 训练时 critic 可见特权状态，而部署策略 actor 只使用可测观测。 | 摘要 |
| proximal policy optimization (PPO) | 近端策略优化（PPO） | translate-with-English | 一种策略梯度强化学习算法。 | III |
| reward vectorization | 奖励向量化 | translate-with-English | 分别为多项奖励学习价值函数，而非先将奖励压成单一标量。 | 引言 |
| multiplicative action noise | 乘性动作噪声 | translate-with-English | 按动作幅值比例施加随机扰动的策略正则化方法。 | 引言 |
| angular momentum regularization | 角动量正则化 | translate-with-English | 通过惩罚全身角动量约束非期望旋转。 | 引言 |
| mean X-displacement (MXD) | 平均 X 方向位移（MXD） | translate-with-English | 实验报告的前向移动距离指标。 | 实验设置 |
| sim-to-real transfer | 仿真到现实迁移 | translate-with-English | 将仿真训练策略部署到真实机器人。 | II-A |
