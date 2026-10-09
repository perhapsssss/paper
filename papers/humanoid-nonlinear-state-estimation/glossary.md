# 术语表

翻译策略：中文学术表达为主；核心缩写首次出现时给出中英文全称。变量、上下标、公式编号、文献引文编号保留原样。图表题翻译为中文，图内英文标注保留在原图中。

| English term | 中文译法 | 说明 |
|---|---|---|
| humanoid robot | 人形机器人 | 论文研究对象。 |
| center of mass (CoM) | 质心（CoM） | 机器人全身质量分布的质心。 |
| divergence component of motion (DCM) | 运动发散分量（DCM） | 用于描述步态稳定性的状态量。 |
| linear inverted pendulum model (LIPM) | 线性倒立摆模型（LIPM） | 常用的线性简化动力学模型。 |
| spring-loaded inverted pendulum (SLIP) | 弹簧负载倒立摆（SLIP） | 用于步态生成的简化模型。 |
| compliant inverted pendulum (CIP) | 柔顺倒立摆（CIP） | 带虚拟弹簧和阻尼器的倒立摆模型。 |
| zero-moment point (ZMP) | 零力矩点（ZMP） | 足底接触力合力矩为零的地面点。 |
| dual-loop Kalman filter (DLKF) | 双环卡尔曼滤波器（DLKF） | 增设扰动估计环路，以补偿模型误差。 |
| invariant extended Kalman filter (IEKF) | 不变扩展卡尔曼滤波器（IEKF） | 利用李群结构进行状态估计的滤波器。 |
| extended Kalman filter (EKF) | 扩展卡尔曼滤波器（EKF） | 对非线性系统作局部线性化的滤波器。 |
| Kalman filter (KF) | 卡尔曼滤波器（KF） | 状态估计方法。 |
| floating base | 浮动基座 | 无固定世界基座的机器人基体参考系。 |
| force-sensitive resistor (FSR) | 力敏电阻（FSR） | 足底接触力传感器。 |
| force/torque sensor | 力/力矩（F/T）传感器 | 用于直接测量力与力矩的传感器。 |
| center-of-mass dynamics | 质心动力学 | 描述 CoM 运动与地面接触力、外力等关系的动力学。 |
| angular momentum rate | 角动量变化率 | 记作 $\dot L$。 |
| non-zero-mean, non-Gaussian, correlated process error | 非零均值、非高斯且相关的过程误差 | 论文讨论的简化模型误差特征。 |
| root mean square error (RMSE) | 均方根误差（RMSE） | 估计性能指标。 |
| model predictive control (MPC) | 模型预测控制（MPC） | 步态规划方法。 |
| Lie group | 李群 | IEKF 状态表示所依据的数学结构。 |
| group affine | 群仿射 | IEKF 所利用的系统性质。 |
| CAD (computer-aided design) | 计算机辅助设计（CAD） | 机器人几何和质量参数来源。 |
| sagittal plane | 矢状面 | 人体前后方向所在平面。 |
| coronal plane | 冠状面 | 人体左右方向所在平面。 |

## 不确定项

- 原 PDF 的式 (16)–(19) 部分矩阵在版面中与邻栏内容交叠；翻译只转写可辨公式部分，并在译文标注，不猜补缺项。
- 原 PDF 参考文献部分版面完整但篇幅较长；译本将参考文献 [1]–[38] 保留为原文书目信息，并提供原 PDF 定位说明。
- 作者简介所在页的文字与照片排布为多栏交错，译本只概述研究方向，不将每段简介与作者强行配对。
