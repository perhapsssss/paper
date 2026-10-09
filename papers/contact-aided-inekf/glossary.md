# 术语表

| English term | 中文译法 | 策略 | 说明 |
|---|---|---|---|
| invariant extended Kalman filter (InEKF) | 不变扩展卡尔曼滤波器 | translate-with-English | 利用李群对称性构造误差传播与观测更新。 |
| right-invariant EKF (RIEKF) | 右不变扩展卡尔曼滤波器 | translate-with-English | 使用右乘定义的状态估计误差。 |
| quaternion-based EKF (QEKF) | 四元数扩展卡尔曼滤波器 | translate-with-English | 以四元数姿态表示的基线滤波器。 |
| matrix Lie group | 矩阵李群 | translate-with-English | 由矩阵组成、具有光滑群结构的集合。 |
| Lie algebra | 李代数 | translate-with-English | 李群单位元处的切空间及其矩阵表示。 |
| group-affine | 群仿射 | keep-English-first | 使左右不变误差动力学与系统轨迹解耦的动力学性质。 |
| log-linear error dynamics | 对数线性误差动力学 | translate-with-English | 李群误差的对数在李代数上满足线性方程。 |
| adjoint map | 伴随映射 | translate-with-English | 在李代数坐标中描述群共轭作用的线性映射。 |
| contact-aided inertial navigation | 接触辅助惯性导航 | translate-with-English | 融合 IMU、接触状态和运动学测量的导航。 |
| forward kinematics | 正向运动学 | translate-with-English | 根据关节状态计算接触点相对机体的位姿。 |
| world-centric | 世界中心 | translate-with-English | 状态主要在世界坐标系中表达。 |
| robo-centric / body-centric | 机器人中心／机体中心 | translate-with-English | 状态主要在机体坐标系中表达。 |
| concentrated Gaussian on a Lie group | 李群上的集中高斯分布 | translate-with-English | 李代数高斯经指数映射得到的群上分布。 |
| observability | 可观测性 | translate-with-English | 从系统输入和观测中辨识状态的能力。 |
| contact point | 接触点 | translate | 与环境发生接触的足端或其他部位。 |
| Brownian motion model | 布朗运动模型 | translate-with-English | 以白噪声驱动缓慢变化状态的过程模型。 |
| SLAM | 同步定位与建图 | translate-with-English | 同时估计机器人状态和环境地标。 |
| IMU bias | IMU 偏置 | translate | 陀螺仪和加速度计的慢变测量误差。 |
| covariance hull | 协方差范围 | translate | 图中以 3σ 表示的状态不确定性区域。 |
