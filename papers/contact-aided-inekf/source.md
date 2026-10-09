# Extracted source text


<!-- PDF page 1 -->

             Contact-Aided Invariant Extended Kalman Filtering for
                          Robot State Estimation*

                  Ross Hartley†    Maani Ghaffari†    Ryan M. Eustice†     Jessy W. Grizzle†

                                        November 13, 2019
2019                                                            Abstract

                      Legged robots require knowledge of pose and velocity in order to maintain stability and execute walking paths.
                      Current solutions either rely on vision data, which is susceptible to environmental and lighting conditions, or fusion ofNov               kinematic and contact data with measurements from an inertial measurement unit (IMU). In this work, we develop a
                       contact-aided invariant extended Kalman ﬁlter (InEKF) using the theory of Lie groups and invariant observer design.
                      This ﬁlter combines contact-inertial dynamics with forward kinematic corrections to estimate pose and velocity along10
                      with all current contact points. We show that the error dynamics follows a log-linear autonomous differential equation
                      with several important consequences: (a) the observable state variables can be rendered convergent with a domain
                       of attraction that is independent of the system’s trajectory; (b) unlike the standard EKF, neither the linearized error
                    dynamics nor the linearized observation model depend on the current state estimate, which (c) leads to improved
                     convergence properties and (d) a local observability matrix that is consistent with the underlying nonlinear system.
                      Furthermore, we demonstrate how to include IMU biases, add/remove contacts, and formulate both world-centric and[cs.RO]                robo-centric versions. We compare the convergence of the proposed InEKF with the commonly used quaternion-based
               EKF though both simulations and experiments on a Cassie-series bipedal robot.  Filter accuracy is analyzed using
                    motion capture, while a LiDAR mapping experiment provides a practical use case. Overall, the developed contact-
                      aided InEKF provides better performance in comparison with the quaternion-based EKF as a result of exploiting
                     symmetries present in system.

           1.  Introduction

            Legged robots have the potential to transform the logistics and package delivery industries, become assistants in our
             homes, and aide in search and rescue [29].  In order to develop motion planning algorithms and robust feedback
                controllers for these tasks, accurate estimates of the robot’s state are needed. Some states, such as joint angles, can be
                directly measured using encoders, while other states, such as the robot’s pose and velocity, require additional sensors.
            Most legged robots are equipped with an inertial measurement unit (IMU) that can measure linear acceleration and
              angular velocity, albeit with noise and bias perturbations. Consequently, nonlinear observers are typically used to fuse
               leg odometry and inertial measurements to infer trajectory, velocity, and calibration parameters [68, 14, 35, 53]. InarXiv:1904.09251v2
             view of a practical solution, designing a globally convergent observer is sacriﬁced for one with at best local properties,
             such as the extended Kalman ﬁlter (EKF) [42, 52, 79, 75]. This EKF-based approach is computationally efﬁcient
             and easily customizable, allowing successful implementation on a number of legged robots with rigorous real-time
             performance requirements [15, 17, 36, 65].
                 Accurate pose estimation can be combined with visual data to build maps of the environment [37]. Then such
            maps can be used in gait selection to improve the stability of a robot while walking on uneven terrains and as a basis
                for high-level motion planning. Although there have been many recent advancements in visual-inertial-odometry
             and simultaneous localization and mapping (SLAM) [66, 48, 38], these algorithms often rely on visual data for pose
               estimation. This means that the observer (and ultimately the feedback controller) can be adversely affected by rapid

                    *Submitted for journal publication. rosshart@umich.edu
                    †Robotics Institute and College of Engineering, University of Michigan, Ann Arbor, MI, USA.


                                                           1

<!-- PDF page 2 -->

changes in lighting as well as the operating environment. It is therefore beneﬁcial to develop a low-level state estimator
that fuses data only from proprioceptive sensors to form accurate high-frequency state estimates.  This approach
was taken by Bloesch et al. [15] when developing a quaternion-based extended Kalman ﬁlter (QEKF) that combines
inertial, contact, and kinematic data to estimate the robot’s base pose, velocity, and a number of contact states. In
this article, we expand upon these ideas to develop an invariant extended Kalman ﬁlter (InEKF) that has improved
convergence and consistency properties allowing for a more robust observer that is suitable for long-term autonomy.
   The theory of invariant observer design is based on the estimation error being invariant under the action of a
matrix Lie group [1, 20], which has recently led to the development of the InEKF1 [18, 8, 10, 11] with successful
applications and promising results in simultaneous localization and mapping [8, 86] and aided inertial navigation
systems [4, 5, 8, 83]. The invariance of the estimation error with respect to a Lie group action is referred to as a
symmetry of the system [5]. Summarized brieﬂy, Barrau and Bonnabel [10] showed that if the state is deﬁned on a
Lie group, and the dynamics satisfy a particular “group afﬁne” property, then the symmetry leads to the estimation
error satisfying a “log-linear” autonomous differential equation on the Lie algebra.  In the deterministic case, this
linear system can be used to exactly recover the estimated state of the nonlinear system as it evolves on the group.
The log-linear property therefore allows the design of a nonlinear observer or state estimator with strong convergence
properties.

1.1.  Contribution

In this article, we derive an InEKF for a system containing IMU and contact sensor dynamics, with forward kinematic
correction measurements. We show that the deﬁned deterministic system satisﬁes the “group afﬁne” property, and
therefore, the error dynamics is exactly log-linear. In practice, with the addition of sensor noise and IMU bias, this
log-linear error system is only approximate; we show, however, that in many cases the proposed InEKF is still preferred
over standard QEKFs due to superior convergence and consistency properties. We demonstrate the utility and accuracy
of the developed observer through a series of LiDAR mapping experiments performed on a Cassie-series biped robot.
    In summary, this work makes the following contributions:

   1. Derivation of a continuous-time right-invariant EKF for an IMU/contact process model with a forward kinematic
     measurement model; the observability analysis is also presented;

   2. State augmentation with IMU biases;

   3. Evaluations of the derived observer in simulation and hardware experiments using a 3D bipedal robot;

   4. Alternative derivation of the observer using a left-invariant error deﬁnition;

   5. Detailed explanation of the connection between the invariant error choice and the world-centric and robo-centric
      estimator formulations;

   6. Equations provided for analytical discretization of the proposed observers; and

   7. Development of an open-source C++ library for aided-inertial navigation using the InEKF https://github.
    com/RossHartley/invariant-ekf.

1.2.  Outline

The remainder of this article is organized as follows. Background and related work are given in section 2.  Sec-
tion 3 provides the necessary preliminary material needed for understanding the InEKF formulation, which is motived
by an example from attitude dynamics in section 4. Section 5 provides the derivation of a right-invariant extended
Kalman ﬁlter (RIEKF) for contact-inertial navigation with a right-invariant forward kinematic measurement model.
In Section 6, we present simulation results comparing the convergence properties to a state-of-the-art QEKF. Sec-
tion 7 discusses the state augmentation of the previously derived InEKF with IMU bias. The consequences of adding
and removing of contact points in the estimator are described in Section 8. Experimental evaluations on a 3D biped

  1We use the InEKF acronym to distinguish from an iterated-EKF (IEKF).


                                              2

<!-- PDF page 3 -->

Figure 1: A Cassie-series biped robot is used for both simulation and experimental results. The robot was developed by Agility Robotics and has
20 degrees of freedom, 10 actuators, joint encoders, and an inertial measurement unit (IMU). The contact and IMU frames used in this work are
depicted above.


robot, shown in Figure 1, are presented in Section 9 along with an application towards LiDAR-based terrain mapping.
Section 10 provides an alternative derivation of the proposed observer using the left-invariant dynamics along with
an explanation of how to easily switch between the two formulations. Section 11 details how these equations can
be modiﬁed to create a “robot-centric” estimator. Section 12 itemizes additional sensor measurements that ﬁt within
the InEKF framework and describes the relation between the developed ﬁlter and landmark-based SLAM. Finally,
Section 13 concludes the article and suggests future directions. Details about time-discretization and useful Lie group
expressions are given in the appendix.

2.  Background and Related work

In this section, we ﬁrst review the Kalman ﬁltering literature to locate the proposed state estimator within the relate
work. Then, we review the state estimation techniques for humanoid and legged robots.

2.1.  Kalman Filtering

Filtering methods involve estimating the robot’s current state (and potentially landmarks) using the set of all measure-
ments up to the current time [2, 41, 73]. When the process model and measurements are linear, and the noise is white
and Gaussian, Kalman ﬁltering [51] provides an optimal method (minimum mean squared error) for state estimation.
The general process for Kalman ﬁltering involves two phases, propagation and correction. The state is typically repre-
sented using a Gaussian random vector, which is parameterized by a mean and a covariance. During the propagation
phase, the previous state and covariance estimate are propagated forward in time using the system dynamics (alterna-
tively known as the process model). When a measurement is obtained, the state and covariance estimate are corrected
using the measurement model along with an associated measurement noise covariance.
   Although the Kalman ﬁlter provides a method for optimal linear ﬁltering, most practical mobile robots have non-
linear system dynamics, and many useful sensor models are also nonlinear. For these cases, an EKF can be designed,
which utilizes Taylor series expansions to linearize the process and measurement models around the current state esti-



                                              3

<!-- PDF page 4 -->

mate [77]. Due to its low computational complexity and accurate performance, the EKF quickly became the de facto
standard of nonlinear ﬁltering for many mobile robot applications, including wheeled vehicles, drones, and legged
robots [24, 70, 15]. The EKFs has also been proposed to solve the SLAM problem [74]. However, since the nonlinear
system is linearized about the current state estimate, the EKF is, at best, only a locally stable observer [76, 52]. The
local convergence proofs are based on Lipschitz bounds of the nonlinear terms in a model, and hence “the more non-
linear a system is, the worse an EKF may perform”. Importantly, if the state estimate is initialized poorly, it is possible
for the ﬁlter to diverge. In addition, because an EKFs uses a systems linearization about the current estimate, states
that are unobservable can spuriously be treated as observable by the ﬁlter. While, this can be mitigated through the
use of an observability-constrained EKF developed by Huang et al. [49], it cannot be altogether avoided.
   For many systems, the error-state (or indirect) EKF offers superior performance to the standard (total state or
direct) form. As the name implies, the error-state extended Kalman ﬁlter (ErEKF) is formulated using the errors,
such as pose and velocity errors, as the ﬁlter variables, while the standard EKF tracks the states themselves (pose and
velocity directly) [59, 69, 79, 75]. Under small noise assumptions, this leads to linear error dynamics which are then
used for covariance propagation in the error-state ﬁlter. The measurement model is also rewritten with respect to these
errors. Although the error dynamics are linear in the error variables, they may still depend on the current state estimate,
which if initialized poorly, will degrade the performance of the ﬁlter. However, the approximately linear nature of the
error dynamics may respect the linear assumptions of the original Kalman ﬁlter better than the underlying system
dynamics, which can lead to improved performance [59].
   Perhaps the most important feature of the ErEKF is the ability to circumvent dynamic modeling [69]. This is done
by replacing the potentially complicated process model with a relatively simple IMU integration model (also known as
strapdown modeling) [78, 62, 82]. Essentially, the IMU’s angular velocity and linear acceleration measurements are
integrated to propagate the state estimate, while the covariance is propagated using the error dynamics. Additional (in-
dependent) sensor measurements will correct the estimated error, which can then be used to update the state estimate.
Using this method, there is no longer a need to formulate complicated, platform-speciﬁc dynamics models, which
may require a large number of state variables and is likely to be exceedingly nonlinear. The “strapdown” ErEKFs has
proven to yield highly accurate results (even with a low-cost IMUs) and continues to form the basis of many inertial
navigation systems (INSs) [13, 54, 79, 75, 15].
    In the standard formulation of Kalman ﬁltering theory, the system evolves on Euclidean spaces. However, in
many cases, the state variables we are interested in lie on a manifold. For example, the orientation of a 3D rigid
body is represented by an element of the special orthogonal group, SO(3).  This matrix Lie group is deﬁned by
the set of orthogonal 3 × 3 matrices with a determinant of one. While the matrix contains nine variables, yet the
dimension of the manifold is only three. One common approach is to parameterize SO(3) using local coordinates
such as three Euler or Tait-Bryan angles [39, 71]. This allows the standard ErEKF equations to be applied; however,
these local parameterizations are often arbitrary (and therefore confusing) and contain singularities (the well-known
Gimbal lock problem). Alternatively, it is possible to represent 3D orientation using quaternions, which are a four-
dimensional double cover (a two to one diffeomorphism) of SO(3). Using quaternions eliminates the singularities;
however, modiﬁcations to the standard ErEKF equations have to be made [75, 79]. In brief, while the orientation
is represented by a four-dimensional quaternion, the orientation error has to be deﬁned by a 3−vector (in the Lie
algebra of SO(3)) and the associated covariance by a 3×3 matrix in order to prevent degeneracy. Also, the orientation
corrections are done through quaternion multiplication instead of vector addition. This QEKF 2 has been well studied
and implemented on a number of platforms, ranging from spacecraft [63, 54] to legged robots [15, 68, 36].
     It turns out, many useful robot states can be characterized using matrix Lie groups. Examples include 2D orien-
tation, SO(2), 3D orientation, SO(3), and 3D pose (orientation and position), SE(3). If the state to be estimated is
a matrix Lie group, it is possible to further improve the EKF ﬁltering approach. Bourmaud et al. [22, 23] developed
versions of both discrete and continuous-time EKFs for systems where the state dynamics and measurements evolve
on matrix Lie groups. In these formulations, noise is represented as a concentrated Gaussian on Lie groups [80, 81],
which is a generalization of the multivariate Gaussian distribution. In essence, noise is represented as a Gaussian in the
tangent space about a point on the manifold. This noise is then mapped to the Lie group through the use of the group’s
exponential map, resulting in a decidedly non-Gaussian distribution on the manifold. An improved state estimate is

   2The quaternion-based formulation of EKFs is also sometimes called “multiplicative ﬁltering” (MEKF) due to the orientation correction being
done through quaternion multiplication [60].



                                              4

<!-- PDF page 5 -->

obtained due to the ﬁlter taking into account the geometry and structure of the problem [23].
   Most recently, a new type of EKF has been developed that is rooted in the theory of invariant observer design,
in which the estimation error is invariant under the action of a Lie group [1, 20]. This invariance is referred to as
the symmetries of the system [5]. This work led to the development of the InEKF [18, 8, 10, 11], with successful
applications and promising results in SLAM [8, 86] and aided INSs [21, 4, 5, 8, 83]. Similar to the above mentioned
EKFs on matrix Lie groups, the state is again represented as a matrix Lie group and the noise as a concentrated
Gaussian on the group.
   However, the InEKF exploits available system symmetries to further improve ﬁltering results. The culminating
result of the InEKF states that if a system satisﬁes a “group-afﬁne” property, the estimation error satisﬁes a “log-linear”
autonomous differential equation on the Lie algebra of the corresponding Lie group [11, 8]. In other words, the system
linearization does not depend upon the estimated states. Therefore, one can design a nonlinear state estimator with
strong convergence properties. Surprisingly, many mobile robot state estimation problems can be solved within the
InEKF framework. This includes attitude estimation [18], inertial odometry [11, 8], velocity-aided inertial navigation
[21], landmark-aided navigation [8], GPS and magnetometer-aided navigation [4], and even EKF-based SLAM. In
this article, we extend this class of solutions to contact-aided inertial navigation [46], where forward kinematics is
used to correct an inertial and contact-based process model. This approach successfully allows an InEKF to be used
for legged robot state estimation.

2.2.  Legged Robot and Humanoid State Estimation

Legged robots are a subclass of mobile robots that locomote through direct and switching contact with the environment.
These robots typically contain proprioceptive sensors, such as IMU, joint encoders, and contact sensors. In addition,
some legged robots, especially humanoids, also have access to exteroceptive sensors, namely cameras and LiDARs.
As with all mobile robots, state estimation for legged robots is critical for mapping, planning, designing feedback
controllers, and developing general autonomy. In this section, an overview of notable techniques for legged robot state
estimation is given.
   The simplest approach for estimation of a legged robot’s spatial location and velocity is kinematic dead-reckoning,
otherwise known as kinematic odometry. This involves estimating relative transformations using only kinematic and
contact measurements. In particular, encoder measurements and the kinematics model are used to track the position,
orientation, and velocity of the robot’s base frame based on the assumption that a stance foot remains ﬁxed to the
ground.  Although this method can be easily implemented, the state estimate is typically noisy due to kinematic
modeling errors, encoder noise, and foot slip [67]. When only one foot is in contact with the ground, this “static
contact assumption” may be violated. For example, if the robot has point feet, the stance foot position may remain
ﬁxed, but the foot orientation is free to rotate (without changing the joint angles). Therefore, a gyroscope is often used
to provide angular velocity measurements which allows the robot’s body velocity to be recovered.
    Alternatively, if the terrain is known a priori and at least three noncollinear point feet are on the ground, Lin
et al. [55] showed that the robot’s instantaneous base pose can be computed through kinematics. These kinematic-
based methods have been implemented on a number of legged robots including a planar one-legged hopper [47], the
CMU Ambler hexapod [67], the RHex hexapod [55], and the biped robot MARLO [31, 32]. However, due to the high
amounts of noise coming from encoders and foot slip, the velocity estimate typically needs to be heavily ﬁltered before
becoming usable in the feedback controller [44]. In addition, this noise causes the position and orientation estimates
to drift substantially rendering the estimator impractical for mapping and autonomy tasks.
    Fortunately, legged robots are often equipped with additional sensors such as IMUs, GPS, cameras, or LiDARs
which provide independent, noisy odometry measurements. Much of the literature on legged robot state estimation
focuses on fusing these measurements (potentially with kinematic odometry) using ﬁltering and smoothing methods.
Singh et al. [72] combined inertial measurements with optical ﬂow measurements in a four-phase hybrid EKF. This
required explicit dynamic modeling of the robot in ﬂight, landing, stance, and thrust phases. Lin et al. [56] took a
similar model-based approach and used an EKF to fuse kinematic information with IMU measurements to estimate
the state of a hexapod. Cobano et al. [30] developed an EKF that fuses kinematic odometry and magnetometer readings
with position measurements from a GPS to localize a SILO4 quadruped outdoors. This implementation ﬁxes the issues
with unbounded drift, but cannot operate in GPS-denied environments. If a prior terrain map is known, Chitta et al.



                                              5

<!-- PDF page 6 -->

[28] showed that it is possible to solve the localization problem for legged robots using only proprioceptive sensors and
a particle ﬁlter. The key idea was that if the robot “senses” that a terrain change through kinematics, then this limits
the potential locations the robot can be in a known map. The method was demonstrated on the LittleDog quadruped.
  A breakthrough came in 2012 when Bloesch et al. [15] combined inertial and kinematic measurements in an
observability-constrained ErEKF using the strapdown IMU modeling approach. In this work, no a priori knowledge
of the terrain is assumed, and the IMU integration model completely eliminates the need for dynamic modeling of
the robot. Therefore, the derived ﬁlter equations are general enough to be used on any legged robot. The key idea
was to augment the state vector with the set of all foot positions currently in contact with the environment. During
the prediction phase, the foot contact dynamics are assumed to be Brownian motion, which can account for some
foot slippage. In the correction phase, forward-kinematic position measurements are used to correct the estimated
state. This work was conducted on the StarlETH quadruped robot. If the stance feet orientations also remain constant,
as is the case for many humanoids, Rotella et al. [68] showed that this ErEKF can be extended to allow forward-
kinematic orientation measurements. The same group also formulated a similar unscented Kalman ﬁlter that uses
forward-kinematic velocity measurements to correct inertial predictions and to accurately detect foot slip [16]. A
detailed analysis of these ﬁltering techniques combined with methods for incorporating computer vision can be found
in Bloesch [17]. Due to the complexity involved in accurately formulating dynamic models, many groups have since
adopted this IMU motion model approach to legged robot state estimation [84, 36, 46].
   This combined inertial and kinematic ﬁltering approach yields an estimate of the robot’s base pose and velocity.
However, some legged robots require additional states to be estimated. Hwangbo et al. [50] formulated a probabilistic
contact estimator for cases when contact sensors are unavailable. Xinjilefu et al. [84] developed a decoupled EKF
that is able to estimate the full state of the humanoid robot ATLAS, including base states, joint angles, and joint
velocities. Using proprioceptive sensing only, Bloesch et al. [15] proved that the absolute positions and yaw angles are
unobservable. Thus, over time, estimates of these quantities will drift unboundedly. This is unacceptable for global
mapping and planning algorithms; however, local elevation maps can still be obtained [37]. Fallon et al. [36] proposed
a method for drift-free state estimation for the humanoid ATLAS. In their implementation, inertial and kinematic
measurements were fused to yield accurate odometry. Point cloud data from a LiDAR sensor was used with a particle
ﬁlter to localize the robot into a pre-built map. This approach provided corrections of position and yaw to obtain a
drift-free estimate of the state. Nobili et al. [64] took a similar approach but used the Iterative Closest Point (ICP)
algorithm to perform LiDAR-based point cloud matching. The algorithm was tested on the HyQ quadruped robot.
    In this article, we propose using an InEKF to estimate the base pose and velocity of a general legged robot. The
approach we take is most similar to Bloesch et al. [15], however we model the entire state as a single matrix Lie group
as opposed to a decoupled state approach. This allows us to take advantage of the geometry and symmetry of the
estimation problem to formulate autonomous error dynamics. In addition with our formulation, the linearizations are
independent of the state estimate resulting in improved convergence properties, especially for poor state initializations.
We formulate both world-centric and robo-centric state estimators highlighting the relation between the left- and right-
invariant error dynamics. In addition, we provide exact analytical time-discretizations of both ﬁlters. The implemented
ﬁlters can be run at high speeds (> 2000 Hz) and can be directly used for accurate local odometry. We demonstrate
this idea through a LiDAR terrain mapping application on a Cassie-series biped robot.

3.  Theoretical background and preliminaries

We assume a matrix Lie group [43, 27] denoted G and its associated Lie Algebra denoted g. If elements of G are n×n
matrices, then so are elements of g. When doing calculations, it is very convenient to let

                                             (·)∧: Rdimg →g

be the linear map that takes elements of the tangent space of G at the identity to the corresponding matrix representation
so that the exponential map of the Lie group, exp : Rdimg →G, is computed by
                                        exp(ξ) = expm(ξ∧),

where expm(·) is the usual exponential of n × n matrices.


                                              6

<!-- PDF page 7 -->

  A process dynamics evolving on the Lie group with state at time t, Xt ∈G, is denoted by

                                    d
                                       dtXt = fut(Xt),
and ¯Xt is used to denote an estimate of the state. The state estimation error is deﬁned using right or left multiplication
of X−1t  as follows.
Deﬁnition 1 (Left and Right Invariant Error). The right- and left-invariant errors between two trajectories Xt and ¯Xt
are:
                          ηrt = ¯XtX−1t = (¯XtL)(XtL)−1   (Right-Invariant)
                                                                                                                      (1)
                              ηlt = X−1t  ¯Xt = (L¯Xt)−1(LXt),   (Left-Invariant)

where L is an arbitrary element of the group.

   The following two theorems are the fundamental results for deriving an InEKF and show that by correct parametriza-
tion of the error variable, a wide range of nonlinear problems can lead to linear error equations.

Theorem 1 (Autonomous Error Dynamics [10]). A system is group afﬁne if the dynamics, fut(·), satisﬁes:

                         fut(X1X2) = fut(X1)X2 + X1fut(X2) −X1fut(Id)X2                             (2)

for all t > 0 and X1, X2 ∈G. Furthermore, if this condition is satisﬁed, the right- and left-invariant error dynamics
are trajectory independent and satisfy:

                     d
                                            t = gut(ηrt)  where  gut(ηr) = fut(ηr) −ηrfut(Id)                       dtηr
                     d
                                            t = gut(ηlt)  where  gut(ηl) = fut(ηl) −fut(Id)ηl                        dtηl


    In the above, Id ∈G denotes the group identity element; to avoid confusion, we use I for a 3 × 3 identity matrix,
and In for the n × n case. The following statements hold for both the left- and right-invariant error dynamics.
   Deﬁne At to be a dimg × dimg matrix satisfying
                                    gut(exp(ξ)) ≜(Atξ)∧+ O(||ξ||2).

For all t ≥0, let ξt be the solution of the linear differential equation

                                      d
                                            dtξt = Atξt.                                                  (3)

Theorem 2 (Log-Linear Property of the Error [10]). Consider the right-invariant error, ηt, between two trajectories
(possibly far apart). For arbitrary initial error ξ0 ∈Rdimg, if η0 = exp(ξ0), then for all t ≥0,

                                            ηt = exp(ξt);

that is, the nonlinear estimation error ηt can be exactly recovered from the time-varying linear differential equation
(3).

   This theorem states that (3) is not the typical Jacobian linearization along a trajectory because the (left- or) right-
invariant error on the Lie group can be exactly recovered from its solution. This result is of major importance for the
propagation (prediction) step of the InEKF [10], where in the deterministic case, the log-linear error dynamics allows
for exact covariance propagation.

Remark 1. This indirect way of expressing the Jacobian of gut is from Barrau and Bonnabel [10]; it is used because
we are working with a matrix Lie group viewed as an embedded submanifold of a set of n × n matrices.


                                              7

<!-- PDF page 8 -->

   During the correction step of a Kalman ﬁlter, the error is updated using incoming sensor measurements. If these
observations take a particular form, then the linearized observation model and the innovation will also be autonomous
[10]. This happens when the measurement, Yt, can be written as either

                          Yt = Xtb + Vt     (Left-Invariant Observation)  or
                                                                                                                      (4)
                          Yt = X−1t b + Vt   (Right-Invariant Observation),

where b is a constant vector and Vt is a vector of Gaussian noise.
   The adjoint representation plays a key role in the theory of Lie groups and through this linear map we can capture
the non-commutative structure of a Lie group.

Deﬁnition 2 (The Adjoint Map, see Hall [43] page 63). Let G be a matrix Lie group with Lie algebra g. For any
X ∈G the adjoint map, AdX : g →g, is a linear map deﬁned as AdX(ξ∧) = Xξ∧X−1. Furthermore, we denote the
matrix representation of the adjoint map by AdX.

   For more details on the material discussed above, along with the theory and proofs about the InEKF, we refer
reader to Barrau [8], Barrau and Bonnabel [10, 11].

4. A motivating example: 3D orientation propagation

Suppose we are interested in estimating the 3D orientation of a rigid body given angular velocity measurements in the
body frame, ˜ωt ≜vec(ωx, ωy, ωz) ∈R3. This type of measurement can be easily obtained from a gyroscope.
   There are several different parameterizations of SO(3); Euler angles, quaternions, and rotation matrices being the
most common.  If we let qt ≜vec(qx, qy, qz) be a vector of Euler angles using the RzRyRx convention, then the
orientation dynamics can be expressed as [33]

                            "qx #   "1   sin(qx) tan(qy)  cos(qx) tan(qy)# "wx #                      d
                                   qy =  0      cos(qx)        −sin(qx)     wy   .
                          dt                                    qz      0   sin(qx) sec(qy)   cos(qx) sec(qy)   wz

Let δqt ≜qt −¯qt ∈R3 be the error between the true and estimated Euler angles. The error dynamics can be written
as a nonlinear function of the error variable, the inputs, and the state

                                  d
                                       dtδqt = g(δqt, ˜ωt, qt).

In order to propagate the covariance in an EKF, we need to linearize the error dynamics at the current state estimate,
qt = ¯qt (i.e. zero error). This leads to a linear error dynamics of the form:

                         0     (ωz¯cx + ωy¯sx)/¯c2y      ¯ty(ωy¯cx −ωz¯sx)                        d
                          dtδqt ≈  0           0                 ωz¯cx + ωy¯sx  δqt
                                  0   (¯sy(ωz¯cx + ωy¯sx))/¯c2y   (ωy¯cx −ωz¯sx)/¯cy
                              ≜A(˜ωt, ¯qt)δqt,

where ¯cx, ¯sx, and ¯tx are shorthand for cos(¯qx), sin(¯qx), and tan(¯qx). The linear dynamics matrix clearly depends
on the estimated angles, therefore bad estimates will affect the accuracy of the linearization and ultimately the perfor-
mance and consistency of the ﬁlter.
  Now instead, let’s use a rotation matrix to represent the 3D orientation, Rt ∈SO(3). The dynamics can now be
simply expressed as
                                    d
                                      dtRt = Rt (˜ωt)× ,





                                              8

<!-- PDF page 9 -->

where (·)× denotes a 3 × 3 skew-symmetric matrix. If we deﬁne the error between the true and estimated orientation
as ηt ≜RTt ¯Rt ∈SO(3), then the (left-invariant) error dynamics becomes

                            d                           T
                                                                 t ¯Rt (˜ωt)× + Rt (˜ωt)×    ¯Rt                               dtηt = RT
                       = RTt ¯Rt (˜ωt)× −(˜ωt)× RTt ¯Rt                                        (5)
                       = ηt (˜ωt)× −(˜ωt)× ηt
                       = g(ηt, ˜ωt).

Using this particular choice of state and error variable yields an autonomous error dynamics function (independent of
the state directly). Since, SO(3) is a Lie Group, we can look at the dynamics of a redeﬁned error that resides in the
tangent space, ηt ≜exp(ξt).

                       d
                            dt(exp(ξt)) = exp(ξt) (˜ωt)× −(˜ωt)× exp(ξt)
                     d
                                  I + (ξt)× ≈  I + (ξt)×  (˜ωt)× −(˜ωt)×  I + (ξt)×                         dt
                          d
               =⇒    (ξt)× = (ξt)× (˜ωt)× −(˜ωt)× (ξt)×                               dt
                       = −(˜ωt)× ξt ×
                             d
                 =⇒ dtξt = (−˜ωt)× ξt

After making a ﬁrst-order approximation of the exponential map, the tangent space error dynamics become linear.
In addition, this linear system only depends on the error, not the state estimate directly. In other words, wrong state
estimates will not affect the accuracy of the linearization, which leads to better accuracy and consistency of the ﬁlter.
For SO(3), this effect is well studied and has been leveraged to design the commonly used QEKFs3, [79, 75]. However,
the extension to general matrix Lie groups, called the InEKF, was only recently developed by Barrau and Bonnabel
[10].
    In the above example, we utilized the ﬁrst-order approximation for the exponential map of SO(3); exp(ξt) ≈
I + (ξt)×. In general, one may ask how much accuracy is lost when making this approximation. The surprising result
by Barrau and Bonnabel [10] is that this linearization is, in fact, exact. This is the basis of Theorem 2. If the initial
error is known, the nonlinear error dynamics can be exactly recovered from this linear system.
    Let’s demonstrate this theorem for the SO(3) example. Let η0 = exp(ξ0) be the initial left invariant error. We can
show that ηt = RTt η0Rt is a solution to the error dynamics equation (5) through differentiation.

                           d
                                                               t η0Rt (˜ωt)× −(˜ωt)× RTt η0Rt                               dtηt = RT
                      = ηt (˜ωt)× −(˜ωt)× ηt

Once we replace the group error with the tangent space error and use the group’s adjoint deﬁnition to shift the rotation
inside the exponential, we arrive at a simple expression for the tangent space error.

                                        ηt = RTt η0Rt
                        =⇒exp(ξt) = RTt exp(ξ0)Rt = exp(RTt ξ0)
                      =⇒ξt = RTt ξ0

Our ﬁnal log-linear error dynamics can now be obtained by differentiating this new error expression.

                                  d
                                                                                        t ξ0                                        dtξt = −(˜ωt)× RT
                           = −(˜ωt)× ξt

   3The set of quaternions, along with quaternion multiplication, actually forms a Lie group.


                                              9

<!-- PDF page 10 -->

Again, this result shows that if the initial error is known, the nonlinear error dynamics can be exactly recovered from
this linear system. In this work, we leverage these ideas to develop a contact-aided inertial observer for legged robots.

5.  SEN+2(3) Continuous Right-Invariant EKF

In this section, we derive a right-invariant extended Kalman ﬁlter (RIEKF) using IMU and contact motion models with
corrections made through forward kinematic measurements. This RIEKF can be used to estimate the state of a robot
that has an arbitrary (ﬁnite) number of points in contact with a static environment. While the ﬁlter is particularly useful
for legged robots, the same theory can be applied for manipulators as long as the contact assumptions (presented in
Section 5.2) are veriﬁed.
    In order to be consistent with the standard InEKF theory, IMU biases are neglected for now. Section 7 provides a
method for reintroducing the bias terms.

5.1.  State Representation

As with typical aided inertial navigation, we wish to estimate the orientation, velocity, and position of the IMU (body)
in the world frame [58, 38, 85]. These states are represented by RWB(t), WvB(t), and WpWB(t) respectively. In addition,
we append the position of all contact points (in the world frame), WpWCi(t), to the list of state variables. This is similar
to the approach taken in Bloesch et al. [15], Bloesch [17].
   The above collection of state variables forms a matrix Lie group, G. Speciﬁcally, for N contact points, Xt ∈SEN+2(3)
can be represented by the following matrix:

                  RWB(t)  WvB(t)  WpWB(t)  WpWC1(t)    · · ·  WpWCN (t)
                                   01,3      1       0         0          · · ·      0
                                   01,3      0       1         0          · · ·      0
                  Xt ≜    01,3      0       0         1          · · ·      0          .
                                                                                                                                                                       ...                                            ...                                                ...                                                      ...         ...                                     ...                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                   01,3      0       0         0          · · ·      1

This Lie group is an extension of SE(3) and has been previously used to solve inertial navigation [8] and SLAM
problems [19, 9]. In fact, the estimators derived in this work have a connection to the landmark-based SLAM problem.
This connection is detailed later in Section 12.
   Because the process and measurements models for each contact point, WpWCi(t), are identical, without loss of
generality, we will derive all further equations assuming only a single contact point. Furthermore, for the sake of
readability, we introduce the following shorthand notation:

                      Rt   vt  pt  dt 
                                       01,3  1   0   0           B ˜ωWB(t)       ˜ωt
                       Xt ≜                        ut =       ≜         ,                                       01,3  0   1   0             B˜aWB(t)          ˜at                                                                                          ,
                                       01,3  0   0   1

where the input ut is formed from the angular velocity and linear acceleration measurements coming from the IMU.
It is important to note that these measurements are taken in the body (or IMU) frame. The Lie algebra of G, denoted
by g, is an N + 5 dimensional square matrix. We use the hat operator, (·)∧: R3N+9 →g, to map a vector to the
corresponding element of the Lie algebra. In the case of a single contact, for example, this function is deﬁned by:

                              ξR     ξv  ξp  ξd 
                                    ×
                       ξ∧=    01,3    0   0   0                                            (6)
                                                      01,3    0   0   0                                                                                                                                                             ,
                                                      01,3    0   0   0



                                              10

<!-- PDF page 11 -->

where (·)× denotes a 3 × 3 skew-symmetric matrix. The inverse operation is deﬁned using the wedge operator,
(·)∨: g →R3N+9. The matrix representation of the adjoint is given by:

                               R     0   0   0 
                                             (vt)× Rt  Rt   0   0
                              AdXt =                                                                     (7)                                            (pt)× Rt   0   Rt   0                                                                                                                          .
                                            (dt)× Rt   0   0   Rt

A closed form expression for the exponential map of SEN+2(3) is given in Appendix B.

5.2.  Continuous-Time System Dynamics

The IMU measurements are modeled as being corrupted by additive Gaussian white noise processes, per

                                     ˜ωt = ωt + wgt ,    wgt ∼GP (03,1, Σg δ(t −t′))
                                                  ˜at = at + wat ,    wat ∼GP (03,1, Σa δ(t −t′)) ,

where GP denotes a Gaussian process and δ(t −t′) denotes the Dirac delta function. These are explicit measurements
coming directly from a physical sensor. In contrast, the velocity of the contact point is implicitly inferred through
a contact sensor; speciﬁcally, when a binary sensor indicates contact, the position of the contact point is assumed to
remain ﬁxed in the world frame, i.e. the measured velocity is zero. In order to accommodate potential slippage, the
measured velocity is assumed to be the actual velocity plus white Gaussian noise, namely

                            W˜vC = 03,1 = CvC + wvt ,  wvt ∼GP (03,1, Σv δ(t −t′)) .

Using the IMU and contact measurements, the individual terms of the system dynamics can be written as:

                                 d
                                                                                       t )×                                   dtRt = Rt (˜ωt −wg
                                 d
                                                                                     t ) + g                                        dtvt = Rt(˜at −wa                                                                                                                      (8)
                                 d
                                       dtpt = vt
                                 d
                                                                                            t ),                                       dtdt = Rt hR(˜αt)(−wv

where g is the gravity vector and  hR(˜αt) is the measured orientation of the contact frame with respect to the IMU
frame as computed through encoder measurements, ˜αt ∈RM, and forward kinematics. Therefore, Rt hR(˜αt) is a
rotation matrix that transforms a vector from the contact frame to the world frame.
    In matrix form, the dynamics can be expressed as
         Rt (˜ωt)×   Rt˜at + g   vt   03,1    Rt   vt  pt  dt  (wgt )×  wat   03,1   hR(˜αt)wvt 
     d            01,3        0      0   0        01,3  1   0   0      01,3    0    0       0
                                                          01,3  0   1   0                    01,3        0      0   0                                                                                  01,3    0    0       0     dtXt =                                                −                                                                                                                                                                                                                                                                                                                                              (9)
                    01,3        0      0   0        01,3  0   0   1      01,3    0    0       0
         ≜fut(Xt) −Xtwt ∧,
with wt ≜vec(wgt , wat , 03,1, hR(˜αt)wvt ). The deterministic system dynamics, fut(·), can be shown to satisfy the
group afﬁne property, (2). Therefore, following Theorem 1, the left- and right-invariant error dynamics will evolve
independently of the system’s state.
   Using Theorem 1, the right-invariant error dynamics is

                         d                                −1
                                                   t = fut(ηrt) −ηrtfut(Id) + (¯Xtwt ∧¯Xt  )ηrt                           dtηr                                                                                                             (10)
                              ≜gut(ηrt) + ¯w∧t ηrt


                                              11

<!-- PDF page 12 -->

where the second term arises from the additive noise. The derivation follows the results in Barrau and Bonnabel [10]
and is not repeated here.
   Furthermore, Theorem 2 speciﬁes that the invariant error satisﬁes a log-linear property. Namely, if At is deﬁned
by gut(exp(ξ)) ≜(Atξ)∧+ O(||ξ||2), then the log of the invariant error, ξ ∈Rdimg, approximately satisﬁes4 the
linear system

                             d
                                  dtξt = Artξt + ¯wt = Atξt + Ad¯Xtwt                                  (11)
                                 ηrt = exp(ξt).

To compute the matrix At, we linearize the invariant error dynamics, gut(·), using the ﬁrst order approximation
ηrt = exp(ξt) ≈Id + ξt ∧to yield

gut(exp(ξt)) ≈
                                                                                                                    I + ξRt        I + ξRt                                                                      ˜at + g  ξvt   03,1                                                                         ξvt  ξpt  ξdt  (˜ωt)×    ˜a + g   03,1   03,1                      (˜ωt)×     I + ξRt                                                    ×           ×                           ×
                01,3                  0           0    0  −      03,1      1   0   0
                                                                                          0                                                                                                0                                                                                                     0                                                                                                           01,3                                                                     0                                                                         1                                                                             0                                                                              03,1                                                                                                                                                                                                                                                                          0           0                                                  0                01,3                                                                                                                                                                                                                                                                                                                                                             01,3     0     0    0                                                                                                                                                                                                                                                                                                   0                                                                                                0                                                                                                     0                                                                                                           01,3                                                                     0                                                                         0                                                                             1                                                                              03,1                                 0                                             0                                                  0                01,3
                                          ∧
       03,3  (g)× ξRt   ξvt   03,1     03,1 
              01,3     0     0    0       (g)× ξRt
              01,3     0     0    0                                     =                                           ξvt           =                                                                 .
              01,3     0     0    0           03,1
                                                                                                             (12)
   With the above, we can express the prediction step of the RIEKF. The state estimate, ¯Xt, is propagated though the
deterministic system dynamics, while the covariance matrix, Pt, is computed using the Riccati equation [61], namely,

                        d               d
                                          ¯Xt = fut(¯Xt) and   = AtPt + PtATt + ¯Qt,                            (13)                             dt                dtPt
where the matrices At and ¯Qt are obtained from (12) and (11),

                      0    0  0  0 
                               (g)×  0  0  0
                               0     I  0  0                                                         and ¯Qt = Ad¯XtCov (wt) AdT¯Xt.                        (14)                       At = 
                               0    0  0  0

Remark 2. For the right-invariant case, expression (14), At is time-invariant and the time subscript could be dropped.
However, in general it can be time-varying, therefore, we use At throughout the paper.

5.3.  Right-invariant Forward Kinematic Measurement Model
Let αt ∈RM denote the vector of joint positions (prismatic or revolute) between the body and the contact point. We
assume that the encoder measurements at time t are corrupted by additive white Gaussian noise.

                                            ˜αt = αt + wαt ,  wαt ∼N(0M,1, Σα)                                  (15)

Using forward kinematics, we measure the relative position of the contact point with respect to the body,

                             BpBC(t) ≜hp(˜αt −wαt ) ≈hp(˜αt) −Jp(˜αt)wαt ,                            (16)

where Jp denotes the analytical Jacobian of the forward kinematics function. Using the state variables, the forward-
kinematics position measurement becomes

                                       hp(˜αt) = RTt (dt −pt) + Jp(˜αt)wαt .                                  (17)

   4With input noise, Theorem 2 no longer holds, and the linearization is only approximate.


                                              12

<!-- PDF page 13 -->

Re-written in matrix form, this measurement has the right-invariant observation form (4),

             hp(˜αt)   RTt  −RTt vt  −RTt pt  −RTt dt  03,1   Jp(˜αt)wαt 
                    0          01,3     1       0       0       0          0                 =                        +                     .
                    1          01,3     0       1       0       1          0                                                                                                                                                     
               −1         01,3     0       0       1     −1         0
                                                                             b  }  |    {zVt    }                  |   {zYt   }   |             X−1{zt               } | {z

Therefore, the innovation depends solely on the invariant error and the update equations take the form [10, Section
3.1.2]
                                            ¯X+t = exp Lt  ¯XtYt −b   ¯Xt
                                                                                                             (18)
                            ηr+t = exp Lt ηrtb −b + ¯XtVt  ηrt,

where exp(·) is the exponential map corresponding to the state matrix Lie group, G, Lt is a gain matrix to be deﬁned
later, bT =  01,3  0  1  −1  , and YTt =  hTp(˜αt)  0  1  −1  . Because the last three rows of ¯XtYt −b are identically
zero, we can express the update equations using a reduced dimensional gain, Kt, and an auxiliary selection matrix
Π ≜  I   03,3  , so that Lt  ¯XtYt −b = KtΠ ¯XtYt as detailed in Barrau [8].
   Using the ﬁrst order approximation of the exponential map, ηrt = exp(ξt) ≈Id + ξt ∧, and dropping higher-order
terms, we can linearize the update equation (18),
                               03,1     Jp(˜αt)wαt ∧
                                                ∧    0            0                                                                                                                                                                                             .                                                                                                 ηr+t  ≈Id + ξ+t ∧≈Id + ξt ∧+                                                                                   1                                                                      0                                                                       + ¯Xt                                                                                                                                                                                                                                                                                         KtΠ                                                                                   Id + ξt      
                                            −1            0

Therefore,

                                                                                ∧                                                                                                                                                                                                                                                                                                       I +                                                                                         03,1                                                                                                                                                                                                                                                      t   ξp                                                                                              t                                                                                        t   ξd                                                                                         Jp(˜αt)wα                                                                                                                             t                                          ξRt ×   ξv
                                                                        0                                                                                     0                                                                                                                                                                                                             1                                                             0                                                                  0                                                            03,1                                                                                                                                                                   ξ+t ∧ = ξt ∧+                                                                        1                                                                                     0                                                                                                                                                                                                                                                                                                                             + ¯Xt                                                                                                                                                                                                                                                                                                                     0                                                             1                                                                  0                                                            03,1                                                                                                                                                                                                                                                                                                                                                                                      KtΠ                                                                                                                                                                −1                                                                                     0                                                         0                                                             0                                                                  1                                                            03,1
                                                             ∧
                     ξpt −ξdt     Jp(˜αt)wαt  
                                         0              0                                                                                                                                                            .                                                                                                                                                   0                                         1                                                                                                                                                                                                                             = ξt ∧+ KtΠ                                                                            + ¯Xt 
                               −1             0

Taking (·)∨of both sides yields the linear update equation,
                    ξ+t = ξt −Kt   03,3   03,3  −I   I  ξt −¯Rt(Jp(˜αt)wαt )
                     ≜ξt −Kt Htξt −¯Rt Jp(˜αt)wαt     .

Finally, we can write down the full state and covariance update equations of the RIEKF using the derived linear update
equation and the theory of Kalman ﬁltering [61, 2, 3] as
                                       ¯X+t = exp KtΠ ¯XtYt  ¯Xt
                                                                                                             (19)
                       P+t = (I −KtHt)Pt(I −KtHt)T + Kt ¯NtKTt ,

where the gain Kt is computed using
                                    St = HtPtHTt + ¯Nt    Kt = PtHTt S−1t
and from (19), the matrices Ht and ¯Nt are given by

                             Ht =  03,3   03,3  −I   I  ,
                                                            T                                  (20)
                                            ¯Nt = ¯Rt Jp(˜αt) Cov(wαt ) JTp(˜αt) ¯Rt .


                                              13

<!-- PDF page 14 -->

5.4.  Observability Analysis

Because the error dynamics are log-linear (c.f., Theorem 2), we can determine the unobservable states of the ﬁlter
without having to perform a nonlinear observability analysis [8]. Noting that the linear error dynamics matrix in our
case is time-invariant and nilpotent (with a degree of 3), the discrete-time state transition matrix is a polynomial in At,

                                       I       0   0  0 
                                               (g)× ∆t      I   0  0
                Φ = expm(At∆t) =  1
                                                (g)× ∆t2  I∆t   I  0                                                                                                                                    2                                            .
                                                 0       0   0   I

It follows that the discrete-time observability matrix is

                       H        0          0    −I   I 
                   HΦ    −1 (g)× ∆t2   −I∆t   −I   I
                O = HΦ2       2                                               .                               −2 (g)× ∆t2  −2I∆t2  −I   I                                                                                             =                                                                                                                                                                                                                                                                                                         ...                                                                                                                                                                                                                                                                               ...                                                              ...                                    ...                   ...

The last six columns (i.e., two matrix columns) of the observability matrix are clearly linearly dependent, which indi-
cates the absolute position of the robot is unobservable. In addition, since the gravity vector only has a z component,
the third column of O is all zeros. Therefore, a rotation about the gravity vector (yaw) is also unobservable. This
linear observability analysis agrees with the nonlinear observability results of Bloesch et al. [15], albeit with much
less computation. Furthermore, as the error dynamics do not depend on the estimated state, there is no chance of the
linearization spuriously increasing the numerical rank of the observability matrix [8]. This latter effect was previously
known and studied by Bloesch et al. [15], and in order to resolve this problem, an observability-constrained EKF [49]
was developed. In our proposed framework, by default, the discrete RIEKF has the same unobservable states as the
underlying nonlinear system; hence, the developed discrete RIEKF intrinsically solves this problem.

6.  Simulation Results

To investigate potential beneﬁts or drawbacks of the proposed ﬁlter, we compare it against a state-of-the-art quaternion-
based extended Kalman ﬁlter (QEKF), similar to those described by Bloesch et al. [15], Rotella et al. [68].  For
implementation, the ﬁlter equations were discretized; see Appendix A for more details.

6.1.  Quaternion-Based Filter Equations:

The choice of error variables is the main difference between the InEKF and the QEKF. Instead of the right-invariant
error (1), a QEKF typically uses decoupled error states

                                         exp(δθt) ≜RTt ¯Rt
                                                   δvt ≜vt −¯vt
                                                                                                             (21)
                                                δpt ≜pt −¯pt.
                                                δdt ≜dt −¯dt.

Using this deﬁnition of error, the QEKF deterministic error dynamics can be approximated as

                       δθt    −(˜ωt)×   0  0  0  δθt 
                          d   δvt      −¯Rt (˜at)×  0  0  0    δvt
                               dt  δpt         0        I  0  0    δpt                                                                        =                                               ,
                                    δdt         0      0  0  0    δdt


                                              14

<!-- PDF page 15 -->

                                    Table 1: Experiment Discrete Noise Statistics and Initial Covariance

               Measurement Type       noise st. dev.          State Element              initial st. dev.
                 Linear Acceleration      0.04 m / sec2         Orientation of IMU     30.0 deg
                Angular Velocity         0.002 rad / sec       Velocity of IMU        1.0 m / sec
                 Accelerometer Bias      0.001 m / sec3       Position of IMU        0.1 m
                Gyroscope Bias          0.001 rad / sec2      Position of Right Foot   0.1 m
                 Contact Linear Velocity   0.05 m / sec          Position of Left Foot    0.1 m
                   Joint Encoders           1.0 deg            Gyroscope Bias        0.005 rad / sec
                                                             Accelerometer Bias     0.05 m / sec2



while the linearized observation matrix becomes

                                    h  ¯RTt (¯dt −¯pt)     0  −¯RTt   ¯RTt i .                           Ht =
                                      ×

   The above linearizations are clearly dependent on the state estimate. Therefore, when the estimated state deviates
from the true state, the linearizations are potentially wrong, reducing accuracy and consistency in the QEKF. In con-
trast, the deterministic right-invariant error dynamics are exactly log-linear (14). In addition, the linearized observation
matrix for our InEKF (20) is also independent of the state estimate.

6.2.  Convergence Comparison:

A dynamic simulation of a Cassie-series bipedal robot (described in Section 9) was performed in which the robot
slowly walked forward after a small drop, accelerating from 0.0 to 0.3 m / sec. The discrete, simulated measurements
were corrupted by additive white Gaussian noise, which are speciﬁed in Table 1 along with the initial state covariance
values. The same values were used in both simulation and experimental convergence evaluations of the ﬁlters. The
IMU bias estimation was turned off for these simulations. The simulation was performed with MATLAB and Simulink
(Simscape Multibody™) where the simulation environment models ground contact forces with a linear force law
(having a stiffness and damping term) and a Coulomb friction model. A typical walking gait is shown in Figure 2.





     Figure 2: A typical walking gait that is used for ﬁlter comparisons. The Cassie bipedal robot is simulated using Simscape Multibody™.


   To compare the convergence properties of the two ﬁlters, 100 simulations of each ﬁlter were performed using
identical measurements, noise statistics, initial covariance, and various random initial orientations and velocities. The
initial Euler angle estimates were sampled uniformly from −30 deg to 30 deg. The initial velocity estimates were
sampled uniformly from −1.0 m / sec to 1.0 m / sec. The pitch and roll estimates as well as the (body frame) velocity



                                              15

<!-- PDF page 16 -->

Figure 3: A quaternion-based extended Kalman ﬁlter (QEKF) and the proposed right-invariant extended Kalman ﬁlter (RIEKF) were run 100 times
using the same measurements, noise statistics, and initial covariance, but with random initial orientations and velocities. The noisy measurements
came from a dynamic simulation of a Cassie-series biped robot where the robot walks forwards after a small drop, accelerating from 0.0 to
0.3 m / sec. The above plots show the state estimate for the initial second of data, where the dashed black line represents the true state. The
RIEKF (bottom row) converges considerably faster than the QEKF (top row) for all observable states. The estimated yaw angle (not shown) does
not converge for either ﬁlter because it is unobservable. Therefore, to compare convergence, the velocities shown are represented in the estimated
IMU (body) frame.


estimates for both ﬁlters are shown in Figure 3. Although both ﬁlters converge for this set of initial conditions, the
proposed RIEKF converges considerably faster than the standard quaternion-based EKF.

6.3.  Accuracy of Linearized Dynamics

The superior performance of the InEKF over the QEKF comes from the improved accuracy of the linearized error
dynamics. As indicated by Theorem 2, the deterministic error dynamics of the InEKF are actually exact, while the
QEKF version is only an approximation. To demonstrate this, a simulation was performed where propagation of the
true error is compared to the propagation of the linearized error dynamics.
  We ﬁrst analyzed the deterministic dynamics. Given an initial error vector, ξtrue0   , the initial state estimate for the
InEKF was computed using the deﬁnition of right-invariant error (1), and the initial state estimate for the QEKF was
computed using equation (21). The true state was initialized to the identity element. The true and estimated states for
both ﬁlters were then propagated for 1 second (1000 time steps), using randomly sampled IMU measurements. The
error states for both the InEKF and the QEKF were also propagated using their respective linearized error dynamics.
The resulting error, ξtrue1   , between the ﬁnal estimated and true states were computed and compared to the propagated
error states, ξprop1   to yield a measure of linearization accuracy, ∥ξtrue1  −ξprop1  ∥. This test was performed multiple times
while linearly scaling the initial orientation error from vec(0, 0, 0) to vec(π/2, π/2, π/2). The results are shown in
Figure 4.
   As expected, when the initial error is zero, the difference between the true and propagated error is zero. This
indicates that the linearized error dynamics for both the InEKF and the QEKF are correct. As the initial error increases,
the difference between the true and propagated error states for the QEKF grows due to the decreased accuracy of the
linearization. In contrast, the difference between the true and propagated error states for the InEKF are always exactly
zero regardless of the initial error. In other words, assuming the initial error is known, the true propagated state can be
exactly recovered from solving the linearized error dynamics system; see Theorem 2.
    In the non-deterministic case (with sensor noise), Theorem 2 no longer holds. This can be seen in Figure 5, where
the same test was performed, but with sensor noise corrupting the propagated state estimate. The difference between
the true and propagated error is no longer exactly zero for the InEKF. However, the InEKF linearization remains more
accurate due to the reduced sensitivity to initial state errors. This helps to further explain the improved convergence
properties shown in Figure 3.



                                              16

<!-- PDF page 17 -->

Figure 4: Analyzing accuracy of the deterministic error dynamics. This   Figure 5: Difference between the true and propagated errors when mea-
Figure shows the difference between the true error and the propagated   surements contain noise. The log-linear error dynamics of the InEKF are
error as the initial true error increases. The state and errors were propa-  no longer exact.
gated for 1 second using randomly sampled IMU measurements.


6.4.  Covariance Ellipse Comparison

The error states in both the QEKF and the InEKF are assumed to be zero-mean Gaussian random vectors. However,
due to the differing choice of error variables, the state uncertainty will differ.  In the QEKF, all states and errors
are decoupled (21).  For example, the true position only depends on the position estimate and the position error,
p = ¯p + δp. Therefore, the position estimate is a Gaussian centered at ¯p. In contrast, when using the InEKF, the
position and orientation are actually coupled together, X = exp(ξ)¯X. Although ξ is a Gaussian random vector,
after applying the group’s exponential map and matrix multiplication, the state estimate’s uncertainty distribution is
no longer Gaussian. This distribution is known as a concentrated Gaussian on a Lie group [80, 81]. This type of
distribution can often capture the underlying system uncertainty better than a standard Gaussian deﬁned in Euclidean
space [57, 7].
   To demonstrate the difference, a simple simulation was performed where the Cassie robot walked forward for
8 sec at an average speed of 1 m/s. The standard deviation for the initial position uncertainty was set to 0.1 m about
each axis, while the standard deviation of the initial yaw uncertainty was set to 10 deg. A set of 10,000 particles
sampled from this distribution were propagated forward to represent the robot’s true uncertainty distribution. After
running both the InEKF and the QEKF, particles were sampled from the resulting ﬁlter covariances to provide a
picture of the estimated position uncertainties. This result is shown in Figure 6. The curved position distribution





Figure 6: 10,000 samples taken from the estimated ﬁlter covariances for a simulation where Cassie walked forward with an average speed of 1 m/s.
The position distributions at times 0, 2, 4, 6, and 8 sec are shown.



                                              17

<!-- PDF page 18 -->

comes from the initial yaw uncertainty that continually grows due to its unobservability (Section 5.4). The InEKF
is able to closely match this distribution since the samples are taken in the Lie algebra and are mapped to the group
through the exponential map. This couples the orientation and position errors leading to a curved position distribution.
In contrast, the QEKF position uncertainty can only have the shape of the standard Gaussian ellipse, which may not
represent the true uncertainty well.
   The InEKF can even accurately model the case of complete yaw uncertainty. To demonstrate this, the initial yaw
standard deviation was set to 360 deg, and the same 8 sec simulation was performed. Each ring in Figure 7 shows the
sample position distribution spaced 2 sec apart. This type of uncertainty cannot be captured with a standard Gaussian
covariance ellipse. These examples illustrate that even if the means are identical, the covariance estimate of the InEKF
can provide a more accurate representation of the state’s uncertainty than the standard QEKF.





Figure 7: Samples taken from the InEKF’s estimated position distribution for a walking simulation with a completely uncertain initial yaw angle.
The robot moved forward at an average speed of 1 m/s. Each ring represents the position uncertainty at times 0, 2, 4, 6, and 8 sec.


    In these examples, the initial covariance of all states (except yaw) was small. It is interesting to note what happens
if we remove the dynamics noise and set the covariance for some states to exactly zero (rank-deﬁcient covariance
matrix). In this case, the initial covariance is supported by a subgroup and the InEKF will keep the state estimate
within a time-dependent subset of the Lie group at all times. This theoretical result was proved by Chauchat et al.
[25], Barrau and Bonnabel [12] to create EKFs with state equality constraints.

7. IMU bias augmentation

Implementation of an IMU-based state estimator on hardware typically requires modeling additional states, such as
gyroscope and accelerometer biases. Unfortunately, as noted in Barrau [8], there is no Lie group that includes the
bias terms while also having the dynamics satisfy the group afﬁne property (2). Even though many of the theoretical
properties of the RIEKF will no longer hold, it is possible to design an “imperfect InEKF” that still outperforms the
standard EKF [8].

7.1.  State Representation

The IMU biases are slowly varying signals that corrupt the measurements in an additive manner:

                                  ˜ωt = ωt + bgt + wgt ,    wgt ∼GP (03,1, Σg δ(t −t′))
                                              ˜at = at + bat + wat ,    wat ∼GP (03,1, Σa δ(t −t′)) .



                                              18

<!-- PDF page 19 -->

These biases form a parameter vector that needs to be estimated as part of the RIEKF state,

                                               bg(t)     bgt                                       θt ≜     ≜    ∈R6.                                      (22)                                               ba(t)     bat

The model’s state now becomes a tuple of our original matrix Lie group and the parameter vector, (Xt, θt) ∈G × R6.
The augmented right-invariant error is now deﬁned as

                                        ert ≜(¯XtX−1t   , ¯θt −θt) ≜(ηrt, ζt).                                   (23)

Written explicitly, the right-invariant error is

                    ¯RtRTt     ¯vt −¯RtRTt vt    ¯pt −¯RtRTt pt    ¯dt −¯RtRTt dt 
                                     01,3        1            0            0                     ηrt =                                     01,3        0            1            0                                                                                                                                        ,
                                     01,3        0            0            1

while the parameter vector error is given by

                                                                            ¯bgt −bgt     ζgt
                                          ζt =   a    ≜         .                                                                            ¯bt −bat     ζat

7.2.  System Dynamics

With IMU biases included, the system dynamics are now expressed as

                               d
                                                                                   t −wgt )×                                 dtRt = Rt (˜ωt −bg
                                d
                                                                                  t −wat ) + g                                      dtvt = Rt(˜at −ba                                                                                                             (24)
                                d
                                     dtpt = vt
                                d
                                                                                         t ).                                     dtdt = Rt hR(˜αt)(−wv

   The IMU bias dynamics are modeled using the typical “Brownian motion” model, i.e., the derivatives are white
Gaussian noise, to capture the slowly time-varying nature of these parameters,

                         d
                                                  t = wbgt  ,    wbgt  ∼GP(03,1, Σbg δ(t −t′))                            dtbg                                                                                                             (25)
                         d
                                                  t = wbat  ,    wbat  ∼GP(03,1, Σba δ(t −t′)).                           dtba

The deterministic system dynamics now depend on both the inputs, ut, and the parameters, θt
                             ¯Rt (¯ωt)×   ¯Rt¯at + g    ¯vt   03,1 
                                                      01,3        0      0   0
                                   fut(¯Xt, ¯θt) =                                                      01,3        0      0   0                                                                                                                                     ,
                                                      01,3        0      0   0

where ¯ωt ≜˜ωt −¯bgt and ¯at ≜˜at −¯b at are the “bias-corrected” inputs. To compute the linearized error dynamics, the
augmented right-invariant error (23) is ﬁrst differentiated with respect to time,

                                 d      d     wbgt
                                        dtert =  dtηrt, wbat       .                                        (26)


                                              19

<!-- PDF page 20 -->

After carrying out the chain rule and making the ﬁrst order approximation, ηrt = exp(ξt) ≈Id + ξt ∧, the individual
terms of the invariant error dynamics become

                       d
                               ¯RtRTt ≈  ¯Rt (wgt −ζgt ) ×                           dt
                  d
                                           ¯vt −¯RtRTt vt  ≈(g)× ξRt + (¯vt)× ¯Rt(wgt −ζgt ) + ¯Rt(wat −ζat )                     dt                                                                                                             (27)
                 d
                                        ¯pt −¯RtRTt pt ≈ξvt + (¯pt)× ¯Rt(wgt −ζgt )                     dt
                 d
                                        ¯dt −¯RtRTt dt ≈   ¯dt × ¯Rt(wgt −ζgt ) + ¯Rt hR(˜αt)wvt .                     dt

Importantly, the augmented invariant error dynamics only depends on the estimated trajectory though the noise and bias
errors, ζt (this is expected because when there are no bias errors, there is no dependence on the estimated trajectory).
A linear system can now be constructed from (27) to yield,

                            d  ξt         ξt      Ad¯Xt   012,6                        = At   +               wt,
                                 dt  ζt        ζt      06,12    I6

where the noise vector is augmented to include the bias terms,

                           wt ≜vec(wgt , wat , 03,1, hR(˜αt)wvt , wbgt  , wbat  ).

7.3.  Forward Kinematic Measurements

The forward kinematics position measurement (17) does not depend on the IMU biases. Therefore, the Ht matrix can
simply be appended with zeros to account for the augmented variables. The linear update equation becomes

                      ξ+t       ξt   " Kξt #       ξt                   =   −       Ht     −¯Rt Jp(˜αt)wαt      .
                      ζ+t      ζt    Kζt        ζt

7.4.  Final Continuous RIEKF Equations

The ﬁnal “imperfect” RIEKF equations that include IMU biases can now be written down. The estimated state tuple
is predicted using the following set of differential equations:

                              d
                                                     ¯Xt , ¯θt =  fut(¯Xt, ¯θt), 06,1  .                                    dt

The covariance of the augmented right invariant error dynamics is computed by solving the Riccati equation

                                d
                                                                                      t + ¯Qt,                                    dtPt = AtPt + PtAT
where the matrices At and ¯Qt are now deﬁned using (27),
                         0    0  0  0     −¯Rt      0 
                                  (g)×  0  0  0   −(¯vt)× ¯Rt   −¯Rt
                                   0     I  0  0  −(¯pt)× ¯Rt    0
                           At =                                   0    0  0  0 −  ¯dt × ¯Rt   0
                                                                                                             (28)                                   0    0  0  0      0        0                                                                                                                                                                                                                                                                                                                                        
                                   0    0  0  0      0        0

                                                                T
                                        Ad¯Xt   012,6            Ad¯Xt   012,6                                    ¯Qt =             Cov(wt)                          .                                           06,12    I6               06,12    I6


                                              20

<!-- PDF page 21 -->

The estimated state tuple and its covariance are corrected though the update equations

                                   ¯X+t , θ+t  =  exp Kξt Π ¯XtYt  ¯Xt ,  ¯θt + Kζt Π ¯XtYt
                                                                                                             (29)
                        P+t = (I −KtHt)Pt(I −KtHt)T + Kt ¯NtKTt ,

where the gains Kξt and Kζt are computed from

                                            " Kξt #                               St = HtPtHTt + ¯Nt    Kt =    = PtHTt S−1t   ,                                            Kζt

with the following measurement, output, and noise matrices,

                         YTt =  hTp(˜αt)  0  1  −1  ,
                             Ht = 0  0  −I   I  0  0  ,
                                            ¯Nt = ¯Rt Jp(˜αt) Cov(wαt ) JTp(˜αt) ¯RTt .

Remark 3. The upper-right block of the new linearized dynamics matrix (28) is related to the adjoint of the current
state estimate (7). Intuitively, this maps the bias error (measured in the body frame) to the world frame.

8.  Addition and Removal of Contact Points

Sections 5 and 7 derived the equations for the RIEKF under the assumption that the contact point is unchanging with
time. However, for legged robots, contacts are discrete events that are created and broken as a robot navigates through
the environment. Therefore, it is important to be able to conveniently add and remove contact points states to and from
the observer’s state.

8.1.  Removing Contact Points

To remove a previous contact point from the state, we marginalize the corresponding state variable by simply removing
the corresponding column and row from the matrix Lie group. The corresponding elements of the covariance matrix
are also eliminated. This can be done through a simple linear transformation. For example, if the robot is going from
one contact to zero contacts, then the newly reduced covariance would be computed by

                                           ξRt                            ξRt    I  0  0  0                                                               ξvt                                                              I  0                                                      0                                        ξv                                                                t                                                                                           = 0                                                              ξp                                                                                                  t                                                                                                                                                                                                                                                                                                                     0  0                                                                  I                                                      0                                       ξp                                                                t                                                                                                             (30)                                                             ξd                                                                                                  t
                                       ξnewt ≜M ξt
                        =⇒Pnewt  = M Pt MT.

Remark 4. This marginalization matrix, M, does not depend on the choice of right or left invariant error.

8.2.  Adding Contact Points

When the robot makes a new contact with the environment, the state and covariance matrices need to be augmented.
Special attention needs to be given to initialize the mean and covariance for the new estimated contact point. For
example, if the robot is going from zero contacts to one contact, the initial mean is obtained though the forward
kinematics relation
                                                                   ¯dt = ¯pt + ¯Rt hp(˜αt).                                          (31)


                                              21

<!-- PDF page 22 -->

In order to compute the new covariance, we need to look at the right-invariant error,

                          ηdt = ¯dt −¯RtRTt dt
                   = ¯pt + ¯Rt hp(˜αt) −¯RtRTt dt
                   = ¯pt + ¯Rt hp(˜αt) −¯RtRTt (pt + Rt hp(˜αt −wαt ))
                     ≈ηpt + ¯RtJp(˜αt)wαt
               =⇒ξdt ≈ξpt + ¯RtJp(˜αt)wαt .

Therefore, covariance augmentation can be done using the following linear map,

                      ξRt    I  0  0          0                                       ξRt                                  ξvt      0   I  0              0                                                    ξv                                                                                                               t                                                                                   t                                                                     ξp                                                            0                                       0                                          0                                                          I                                                     t                                                                                                         =                                                                                                                                       +                                                                              wα                                                    ξp                                                                                   t                                                                                                             (32)                                       0                                          0                                                          I                                ξd                                                                        ¯RtJp(˜αt)                                                     t
                                ξnewt  ≜Ft ξt + Gtwαt
                   =⇒Pnewt  = Ft Pt FTt + Gt Cov(wαt ) GTt .

Remark 5. The error augmentation matrix, Ft, and the noise matrix, Gt, will depend on the choice of error variable.
Here they are derived for the right invariant error case. The matrices will differ in the left invariant error formulation,
as detailed in Section 10.

9.  Experimental Results on Cassie Robot

We now present an experimental evaluation of the proposed contact-aided RIEKF observer using a 3D bipedal robot.
The Cassie-series robot, shown in Figure 1, developed by Agility Robotics, has 20 degrees of freedom coming from
the body pose, 10 actuators, and 4 springs. The robot is equipped with an IMU along with 14 joint encoders that
can measure all actuator and spring angles. The proposed and baseline algorithms (along with the robot’s feedback
controller) are implemented in MATLAB (Simulink Real-Time). The IMU (VectorNav-100) is located in the robot’s
torso and provides angular velocity and linear acceleration measurements at 800 Hz. The encoders provide joint angle
measurements at 2000 Hz. The robot has two springs on each leg that are compressed when the robot is standing on
the ground. The spring deﬂections are measured by encoders and serve as a binary contact sensor. The controller used
for these experiments was developed by Gong et al. [40].

9.1.  Convergence Comparison

An experiment was performed where the robot walked forwards at approximately 0.3 m / sec. The QEKF and the
proposed RIEKF were run (off-line) 100 times using the same logged measurements, noise statistics, and initial covari-
ance with random initial orientations and velocities. The noise statistics and initial covariance estimates are provided in
Table 1. As with the simulation comparison presented in Section 6, the initial mean estimate for the Euler angles were
uniformly sampled from −30 deg to 30 deg and the initial mean estimate for velocities were sampled uniformly from
−1.0 m / sec to 1.0 m / sec. Bias estimation was turned on and the initial bias estimate was obtained from processing
the IMU data when the robot was static. The pitch and roll estimates as well as the (body frame) velocity estimates
for both ﬁlters are shown in Figure 8. The “ground truth” trajectory estimates (black lines) were computed by initial-
izing each ﬁlter with a good state estimate at a time before the beginning of the plot (to allow for convergence). The
initial orientation was obtained from the VectorNav-100’s onboard EKF and the initial velocity was obtained through
kinematics alone.
   The experimental results for comparing ﬁlter convergence matches those of the simulation. The proposed RIEKF
converges faster and more reliably in all 100 runs than the QEKF; therefore, due to the convenience of initialization
and reliability for tracking the developed RIEKF is the preferred observer.



                                              22

<!-- PDF page 23 -->

Figure 8: An experiment was performed where an actual Cassie-series robot slowly walked forward at approximately 0.3 m / sec. The noisy
measurements came from the on-board IMU (VN-100) and the robot’s joint encoders. The quaternion-based extended Kalman ﬁlter (QEKF) and
the proposed right-invariant extended Kalman ﬁlter (RIEKF) were run (off-line) 100 times using the same measurements, noise statistics, and initial
covariance, but with random initial orientations and velocities. The black line represents the ﬁlter state estimates when initialized with a good
estimate. The RIEKF (bottom row) converges considerably faster than the QEKF (top row) for all observable states. Zoomed-in plots of the RIEKF
performance is provided in the top-right corner.

   When the state estimate is initialized close to the true value, the RIEKF and QEKF have similar performance (black
lines), because the linearization of the error dynamics accurately reﬂects the underlying nonlinear dynamics. However,
when the state estimate is far from the true value, the simulation and experimental results show that RIEKF consistently
converges faster than the QEKF. The relatively poor performance of the QEKF is due to the error dynamics being
linearized around the wrong operating point, in which case the linear system does not accurately reﬂect the nonlinear
dynamics. In addition, when bias estimation is turned off, the invariant error dynamics of the RIEKF do not depend
on the current state estimate. As a result, the linear error dynamics can be accurately used even when the current state
estimate is far from its true value, leading to better performance over the QEKF. Although this theoretical advantage
is lost when bias estimation is turned on, the experimental results (shown in Figure 8) indicate that the RIEKF still is
the preferred observer due to less sensitivity to initialization.

9.2.  Motion Capture Experiment

In order to verify the accuracy of the InEKF state estimate, we performed a motion capture experiment in the University
of Michigan’s M-Air facility.  This outdoor space is equipped with 18 Qualisys cameras that allows for position
tracking. We had the Cassie robot walk untethered for 60 sec along an approximately 15 m path. A top-down view
of the estimated trajectory is shown in Figure 9. Although there is noticeable drift due to the unobservability of the
position and yaw, the ﬁnal position error accounts for less than 5% of the distance traveled. This drift error is due to
a combination of sensor noise and imperfect modeling of the robot’s kinematics which may introduce biases to the
forward kinematic measurements. The orientation, velocity, and position estimates along with their 3σ covariance
hulls are shown in Figure 10. Due to the unobservability of the yaw angle, the velocity estimate is given in the body
frame instead of the world frame. The orientation is plotted using exponential coordinates, exp(φ) = R. Due to an
inaccurate orientation estimate from the motion capture system, the “ground truth” for the orientation is given by the
VectorNav-100, which runs a state-of-the-art QEKF that fuses angular velocity, linear acceleration, and magnetometer
measurements to estimate orientation only. As expected, the error for all observable states remains small. The absolute
position and the orientation about the gravity vector are unobservable, so some drift will occur for these states. While
the drift is largely imperceptible for φz, it is interesting to note that the covariance slowly grows over time due to
this unobservability. More signiﬁcant drift occurs on the absolute position states. This drift can be attributed to a
combination of sensor noise, foot slip, and kinematic modeling errors.
    In order to plot the 3σ covariance hull, the right-invariant error covariance needed to be converted to a covariance





                                              23

<!-- PDF page 24 -->

Figure 9: Top-down view of the InEKF’s estimated trajectory for a motion capture experiment. The position drift is unobservable, however, the
ﬁnal drift is less than 5% of the distance traveled.


where the error is deﬁned by Euclidean distance. Up to a ﬁrst-order approximation, this mapping is done using:

                      δφt   −Γ−11  (¯φt)   0   0  ξRt 
                                                          δvt =    (¯vt)×    −I   0   ξvt ,                               (33)
                                   δpt          (¯pt)×     0  −I   ξpt

where the “Euclidean orientation error” is deﬁned as δφt ≜φt −¯φt, and the velocity and position errors match the
QEKF error states (21). The matrix Γ1(¯φt) is known as the left Jacobian of SO(3) and has an analytical form. Further
explanation and the derivation of the above equation is given in Appendix C.

9.3.  Long Odometry Experiment

In addition to providing accurate estimates of states vital for legged robot control (orientation and velocity), this InEKF
can also provide reliable odometry for a higher-level mapping or SLAM system. To demonstrate the accuracy of long-
term odometry, we had Cassie walk about 200 m along a sidewalk around the University of Michigan’s Wave Field.
In total, the walk took 7 minutes and 45 seconds. The estimated path from the InEKF overlaid onto Google Earth
imagery is shown in Figure 11. A video of this experiment can be found at https://youtu.be/jRUltB_dMlo.

   Even though the absolute position is unobservable, the odometry estimate from the InEKF contains low enough
drift to keep the estimate on the sidewalk for the duration of the experiment. The ﬁnal position estimate is within a
few meters of the true position, and the yaw drift is imperceptible. This odometry estimate is readily available, as it
only depends on inertial, contact, and kinematic data, which barring sensor failure, always exist. It does not require
the use of any vision systems that may be susceptible to changes in environment or lighting conditions.

9.4.  LiDAR Mapping Application

One application for the InEKF odometry is the building of local maps of the environment. We equipped the Cassie-
series robot with a new torso that houses a Velodyne VLP-32C LiDAR. With the ﬁlter running, we can project each
received packet of point cloud data into the world frame based on the current state estimate. This point cloud data




                                              24

<!-- PDF page 25 -->

Figure 10: Motion capture experiment conducted in the University of Michigan’s M-Air facility. The dashed black line represents ground truth,
the solid red line is the right-invariant EKF estimate, and the red shaded area represents the 3σ covariance hull. The ground truth for position
and velocity were obtained using 18 Qualisys cameras. Due to poor orientation estimates from the motion capture system, the “ground truth”
for orientation was obtained from the VectorNav-100, which runs a highly accurate on-board QEKF. The orientation data is plotted using the
exponential coordinates.
                                              25

<!-- PDF page 26 -->

      Figure 11: Long outdoor odometry experiment where Cassie walked roughly 200 m along a sidewalk over 7 minutes and 45 seconds.


can then be accumulated to create a map of the environment. Figure 12 shows a few still frames from several Li-
DAR mapping experiments. Videos of these results can be viewed at https://youtu.be/pNyXsZ5zVZk and
https://youtu.be/nbQTQw0gJ-k.

10.  Alternative Left-Invariant Formulation

For the derivations in Sections 5-8, we were assuming the use of the right-invariant error. This choice was due to the
forward kinematic measurement having the right-invariant observation form. However, it is possible to derive a left-
invariant form of this ﬁlter, which may be more appropriate to use when dealing with left-invariant observations. For
example, GPS measurements are left-invariant observations for the world-centric observer; see Section 12. Written
explicitly, the left-invariant error is

                       RTt ¯Rt  RTt (¯vt −vt)  RTt (¯pt −pt)  RTt (¯dt −dt)
                                           01,3       1           0           0                    ηlt ≜X−1t  ¯Xt =                                           01,3       0           1           0                                                                                                                                                .
                                           01,3       0           0           1





                                              26

<!-- PDF page 27 -->

     (a) University of Michigan’s North Campus with the bell tower                            (b) Looking towards a staircase





                       (c) Walking along a sidewalk                                      (d) Inside the Bob and Betty Beyster Building

Figure 12: LiDAR maps created by transforming 10 seconds of point cloud data onto the pose trajectory estimated by the InEKF. The high
frequency odometry estimate allows for motion compensation within a single scan of the LiDAR (10Hz); https://youtu.be/pNyXsZ5zVZk
and https://youtu.be/nbQTQw0gJ-k.


After carrying out the chain rule and making the ﬁrst order approximation, ηlt = exp(ξt) ≈Id + ξt ∧, the individual
terms of the left-invariant error dynamics become:

                        d
                       dtRTt ¯Rt ≈  −(˜ωt −ζgt )× ξRt −ζgt + wgt ×
                   d                         a                  g
                                        t (¯vt −vt) ≈−  ˜at −¯bt × ξRt −  ˜ωt −¯bt × ξvt −ζat + wat                  dtRT
                   d                                g
                                        t (¯pt −pt) ≈ξvt −  ˜ωt −¯bt × ξpt                  dtRT
                   d                            g
                                        t (¯dt −dt) ≈−  ˜ωt −¯bt × ξdt + hR(˜αt)wvt .                  dtRT

Using these results, the log-linear left-invariant dynamics can be expressed using the following linear system

                                   d
                                         dtξt = Atξt + wt
                                   d
                                                                                          t + ¯Qt,                     =⇒ dtPt = AtPt + PtAT





                                              27

<!-- PDF page 28 -->

where the dynamics and noise matrices are

                    −(¯ωt)×     0        0        0    −I   0 
                               −(¯at)×  −(¯ωt)×     0        0      0  −I
                               0          I     −(¯ωt)×     0      0   0                      Alt =
                               0        0        0     −(¯ωt)×   0   0                         (34)
                               0        0        0        0      0   0                                                                                                                                                                                                                                                                                                                                                                             
                               0        0        0        0      0   0
                             ¯Qt = Cov(wt).

Similar to the right-invariant case, the dynamics only depend on the state through the IMU bias. When a left-invariant
observation comes in, the state estimate is corrected using
                                ¯X+t , θ+t  =   ¯Xt exp Kξt Π ¯X−1t  Yt    ,  ¯θt + Kζt Π ¯X−1t  Yt   ,                      (35)

where the exponential map is now multiplied on the right side [10].

10.1.  Switching Between Left and Right-Invariant Errors

Because forward kinematic measurements have the right invariant observation form, the innovation equations are only
autonomous when the right invariant error is used. Fortunately, it is possible to switch between the left and right error
forms through the use of the adjoint map.
                                    ηrt = ¯XtX−1t = ¯Xtηlt ¯X−1t
                      =⇒exp(ξrt) = ¯Xt exp(ξlt)¯X−1t = exp(Ad¯Xtξlt)
                     =⇒ξrt = Ad¯Xtξlt

This transformation is exact, which means that we can easily switch between the covariance of the left and right
invariant errors using
                                       Prt = Ad¯Xt Plt AdT¯Xt.                                          (36)
    Therefore, when handling a right-invariant observation, we can map the propagated left-invariant covariance to
the right-invariant covariance temporarily, apply the right-invariant update equations (29), then map the corrected
covariance back to the left-invariant form.
     It is also possible to compute the log-linear left-invariant dynamics starting from the right-invariant form. Substi-
tuting (36) into the (right-invariant) covariance propagation equation (13) and solving for the left-invariant covariance
yields

                       d                         d
                                                                                                            t                          dtPl                                              t =  Ad¯X−1t ArtAd¯Xt −Ad¯X−1t  dt  Ad¯Xt    Pl
                           −d                                               AdT                                                    AdT                                                                                                                 ¯Xt                    + Plt  AdT¯XtArTt AdT¯X−1t                                                                                              ¯X−1t                                                          dt
                                                       r
                    + Ad¯X−1t  ¯Q tAdT¯X−1t   .

Therefore, we learn that the right and left dynamics and noise matrices are related by the following expressions

                                                  d
                               Alt ≜Ad¯X−1t ArtAd¯Xt −Ad¯X−1t  dt  Ad¯Xt                                 (37)
                                                                                       .                                      ¯Q lt ≜Ad¯X−1t  ¯Q rtAdT¯X−1t

Remark 6. Intuitively, the left-invariant error represents an error measured in the body frame of the robot, while the
right-invariant error represents an error measured in the world or spatial frame. The frame of measurement dictates
whether the exponential map appears on the right or left in the update equations. The error can be moved between
these two frames using the adjoint map of the Lie group.


                                              28

<!-- PDF page 29 -->

10.2.  Adding New Contact Points

The process for removing a contact point from the state (marginalization) is identical to the right-invariant error case,
described in Section 8.1.  Likewise, when a new contact is detected, the state can be augmented using the same
kinematics relation (31) as before. However, due to the change in error variable, the process for augmenting the
covariance will be different.
    In order to compute the new covariance, we need to look at the left-invariant error,

                        ηdt = RTt (¯dt −dt)
                  = RTt   ¯pt + ¯Rt hp(˜αt) −RTt (pt + Rt hp(˜αt −wαt ))
                    ≈ηpt + ηRt  hp(˜αt) −hp(˜αt) + Jp(˜αt)wαt
              =⇒ξdt ≈ξpt −( hp(˜αt))× ξRt + Jp(˜αt)wαt .

Therefore, covariance augmentation can be done using the following linear map,

                   ξRt         I       0  0         0                                          ξRt                              ξvt           0         I  0             0                                                           ξv                                                                                                                      t                                                                                             t                                                                                0                                                0                                                                 I                             ξp                                                                 0                                               t                                                                                            =                                                                                                                                                                                                       wα                                  +                                                           ξp                                                                                             t                                                                                                             (38)                                                0                                                                 I                            ξd                                                                            Jp(˜αt)                                    (−hp(˜αt))×                                               t
                            ξnewt  ≜Ft ξt + Gtwαt
                =⇒Pnewt  = Ft Pt FTt + Gt Cov(wαt ) GTt .

11.  Robo-centric Estimator

In this section, we derive a “robot-centric” version of the contact-aided InEKF where the estimated state is measured
in the robot’s base (IMU) frame. When switching to a robot-centric model, the forward kinematics measurements take
the left-invariant observation form. In addition, the left/right-invariant error dynamics equations are identical to the
world-centric form, albeit swapped. The right-invariant error dynamics for the world-centric estimator are equivalent
to the left-invariant error dynamics for the robo-centric estimator.
   The properties of this ﬁlter are identical to the RIEKF derived in Section 5. However, in some cases this ﬁlter may
be preferred as it directly estimates states that are useful for controlling a legged robot (namely the velocity measured
in the body frame).

11.1.  State and Dynamics

We are interested in estimating the same states as before, though measured in the robot’s body frame. Again, the state
variables can form a matrix Lie group, G. Speciﬁcally, for N contact points, Xt ∈SEN+2(3) can be represented by
the following matrix (which is simply the inverse of the world-centric state)5:

                   RBW(t)  −BvB(t)  BpBW(t)  BpC1W(t)    · · ·  BpCNW(t)
                            01×3      1        0        0         · · ·      0
                                        redeﬁne   01×3      0        1        0         · · ·      0
                  Xt ≜    01×3      0        0        1         · · ·      0
                                                                                                                                                                              ...                                                ...                                                  ...                                                    ...         ...                                    ...                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                            01×3      0        0        0         · · ·      1

   5The negative sign on body velocity appears when inverting the world-centric state; −BvB = −RTWB WvB. This sign is removed on the position
vectors by swapping the start and end points, BpBW = −RTWB BpWB.





                                              29

<!-- PDF page 30 -->

Without loss of generality, assume a single contact point. Furthermore, for the sake of readability, we redeﬁne our
shorthand notation to be body-centric states,

                                Rt    vt  pt  dt 
                                                                       redeﬁne  01×3  1   0   0
                                 Xt ≜                                                              (39)                                            01×3  0   1   0                                                                                                                       .
                                            01×3  0   0   1

   Using the bias corrected IMU measurements, the individual terms of the new robot-centric system dynamics can
be derived as [16]

                          d
                                                                         t )× Rt                            dtRt = −(¯ωt −wg
                          d
                                                                        t ) −Rt g −(¯ωt −wgt )× vt                                dtvt = −(¯at −wa                                                                                                             (40)
                          d
                                                                             t )× pt                               dtpt = vt −(¯ωt −wg
                          d
                                                                         t )× dt −hR(˜αt)wvt .                               dtdt = −(¯ωt −wg

Written in matrix form, this becomes

      −(¯ωt)× Rt   −¯at −Rtg −(˜ωt)× vt   vt −(˜ωt)× pt  −(¯ωt)× dt   (wgt )×  wat   03,1   hR(˜αt)wvt   Rt   vt  pt  dt 
 d             01,3              0                0           0             01,3    0    0       0         01,3  1   0   0
                                                                                                                               01,3  0   1   0                01,3              0                0           0                                                                                           01,3    0    0       0 dtXt =                                                                             −                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                01,3              0                0           0             01,3    0    0       0         01,3  0   0   1
     ≜fu(Xt, θt) −wt ∧Xt
                                                                                                             (41)
with wt ≜vec(wgt , wat , 03,1, hR(˜αt)wvt ). The deterministic dynamics function fu(·) can be shown to satisfy the
group afﬁne property (2). Therefore, the left (and right) invariant error dynamics depends solely on the invariant error.
  We can derive the log-linear dynamics matrices for the body-centric estimator following a similar derivation pro-
cess to the world-centric version in Section 5. In fact, without IMU bias, the linearization of the left-invariant dynamics
for the body-centric estimator is the same as the right-invariant dynamics for the world-centric estimator;

                                Alt (body-centric) = Art (world-centric)
                                                                                                             (42)
                            Art (body-centric) = Alt (world-centric).

When IMU bias is included, the above relation still holds, though with the bias terms negated6. The noise covariance
matrices for the body-centric left/right-invariant propagation models are given by:

                                                                 T
                                    Ad¯X−1t    015,6                                                            Ad¯X−1t    015,6                                             Cov(wt)                                  ¯Q lt =
                                           06,15     I6               06,15     I6                                (43)
                                  ¯Q rt = Cov(wt),
which are also swapped versions of the world-centric noise matrices, after accounting for the redeﬁnition of ¯Xt as its
inverse. A comparison of the world-centric and body-centric equations are given in Tables 2 and 3.

11.2.  Left-Invariant Forward Kinematic Measurement Model

We use forward-kinematics to measure the relative position of the contact point with respect to the body,  hp(˜αt).
Using the new robot-centric state variables, the measurement model (16) becomes

                                          hp(˜αt) = pt −dt + Jp(˜αt)wt.                                     (44)

    6If deﬁnition of bias error is negated, even these terms would remain the same.


                                              30

<!-- PDF page 31 -->

Re-written in matrix form, this measurement will have now have the left-invariant observation form (4),

                  hp(˜αt)   Rt   vt  pt  dt   0   Jp(˜αt)wαt 
                           0          01,3  1   0   0    0         0
                     =               +                     .                       (45)
                           1          01,3  0   1   0    1         0                                                                                                                                       
                    −1         01,3  0   0   1   −1         0
                         |   {z   }   |        {z        } | {z }  |    {z    }                          Yt             Xt         b         Vt
The state update equation will take the left-invariant form (35), where the matrices Ht and ¯Nt can be derived to be:

                             Ht =  03,3   03,3   I  −I  ,
                                     T                                                              (46)
                                            ¯Nt = ¯R t Jp(˜αt) Cov(wαt ) JTp(˜αt) ¯Rt.

It is important to note that the forward kinematics measurement is a right-invariant observation for the world-centric
estimator, while the same measurement becomes a left-invariant observation for the body-centric version. Also, the
above linearization (46) is similar to the world-centric, right-invariant one (20). Namely, Ht is simply negated, while
¯Nt is identical after accounting for the redeﬁnition of the state as its inverse.

12.  Additional Sensor Observations

This article extends upon our conference paper results [46] where we originally presented the contact-aided InEKF.
As described in earlier sections, this ﬁlter uses an inertial-contact dynamics model with corrections coming from
forward kinematics. In addition to forward kinematics, other groups have discovered that a number of measurements
common to robotics can also ﬁt the invariant observation model (4). Bonnabel [18] developed an invariant observer
that uses magnetometer and acceleration measurements to solve the attitude estimation problem. Barczyk and Lynch
[4], Barrau [8] described methods for invariant observer design for GPS and magnetometer-aided navigation. Wu et al.
[83] developed an InEKF to solve visual-inertial navigation.  It has also been shown that an InEKF can be used for
SLAM [19, 9, 86].
    In particular, it is interesting to note the similarities between our contact-aided InEKF and landmark-based SLAM.
In the simplest case, this SLAM problem involves jointly estimating the robots state along with the position of static
landmarks in the environment. The robot is often assumed to have a sensor capable of measuring the position of the
landmark relative to the robot. This formulation is identical to our developed InEKF with the contact positions acting
as landmarks and forward kinematics measuring the relative translation between the base and contact frames. This
similarity was also mentioned by Bloesch et al. [15]. However, there are a few notable differences. The contact frame
velocity is assumed to be white noise to allow for foot slip, while landmarks are usually treated as static. Forward
kinematics measurements often come at high frequencies (2000 Hz on Cassie). In contrast, landmarks measurements
are often at a much lower frequency. Finally, with landmark observations, a data association problem often has to be
solved which associates the measurement with a particular landmark state. This problem does not exist with forward
kinematic measurements.
   Due to the similarities between contacts and landmarks, in our state matrix, the contact states could be easily
replaced with landmark states, WpWLi(t),

                  RWB(t)  WvB(t)  WpWB(t)  WpWL1(t)    · · ·  WpWLN (t)
                                   01,3      1       0         0          · · ·      0
                                   01,3      0       1         0          · · ·      0
                   Xt ≜    01,3      0       0         1          · · ·      0          ,
                                                                                                                                                                        ...                                            ...                                                ...                                                      ...         ...                                     ...                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                   01,3      0       0         0          · · ·      1

or a combination of contact and landmark positions. In this way, it is possible to develop an observer that contains
no unobservable states. Of course, like EKF-SLAM, the ﬁlter can become too computationally expensive to run in
real-time if the number of landmarks grows too large.


                                              31

<!-- PDF page 32 -->

   Tables 2 and 3 give a summary of the left/right world-centric and robo-centric InEKF equations assuming a single
contact and landmark position. The linearized observation matrix and observation type for several different sensors
are also provided. In these tables, lt is shorthand for the true landmark position, and m denotes the true magnetic
ﬁeld vector. Using these tables, it is clear to see the relation between the left/right invariant error dynamics and the
world/robo-centric formulations. All of these dynamics and observations are supported in an open-source C++ Library
released alongside this article; available at: https://github.com/RossHartley/invariant-ekf.

13.  Conclusion and future Work

Using recent results on a group-invariant form of the extended Kalman ﬁlter (EKF), this article derived an observer
for a contact-aided inertial navigation system for a 3D legged robot. Contact and IMU sensors are available on all
modern bipedal robots; therefore, the developed system has the potential to become an essential part of such platforms
since an observer with a large basin of attraction can improve the reliability of perception and control algorithms. We
also included IMU biases in the state estimator and showed that, while some of the theoretical guarantees are lost, in
real experiments, the proposed system has better convergence performance than that of a commonly used quaternion-
based EKF. Although the latter is a discrete EKF on a Lie group, it does not exploit symmetries present in the system
dynamics and observation models, namely, invariance of the estimation error under a group action. In addition to the
original right-invariant form of the ﬁlter, the left-invariant dynamics are discussed as well as a robo-centric version of
the ﬁlter.
  A series of experiments were conducted while running the ﬁlter on a Cassie-series biped robot. The accuracy of
the invariant-EKF was demonstrated through a motion capture comparison, while long-term odometry was compared
by overlaying the trajectory on Google Earth imagery. In addition to improving signals used for feedback control,
the pose estimate from this ﬁlter can be used alongside a vision sensor to build maps of the environment. This was
demonstrated on Cassie by building LiDAR-based point cloud maps while walking.
   Future work includes developing an invariant smoother based on this ﬁlter. This would utilize the framework
developed by Chauchat et al. [26] to potentially improve IMU preintegration [58, 38, 34] as well as contact preinte-
gration [45] to perform SLAM. One interesting extension would be online estimation of kinematic parameters, which
may help remove biases in the forward kinematic measurements. Another possibility for improvement of legged robot
odometry is the detection of mode changes such as standing, ﬂat-ground walking, and turning. During these modes,
additional constraints may be inferred, which could improve state estimation [24]. Finally, additional experiments need
to be conducted to explore the potential for visual-inertial-contact odometry using an InEKF as well as incorporating
prior terrain information into the ﬁlter.





                                              32

<!-- PDF page 33 -->

                                          Table 2: Summary of World-centric State Estimator


State Deﬁnition                                                Deterministic Nonlinear Dynamics
     RWB   WvB  WpWB  WpWC  WpWL                     ¯Rt (¯ωt)×    ¯Rt¯at + g     ¯vt   03×1   03×1 
      01×3    1     0      0      0                                  01×3        0      0    0      0
Xt ≜  01×301×3    00     10      01      00                         fut(¯Xt, ¯θt) =    01×301×3        00      00    00      00     
      01×3    0     0      0      1                                  01×3        0      0    0      0

Log-Linear Right-Invariant Dynamics                         Log-Linear Left-Invariant Dynamics
      0     0   0   0   0      −¯Rt        0            −(¯ωt)×       0          0          0          0     −I    0 
      (g)×   0   0   0   0   −(¯vt)× ¯Rt   −¯Rt                   −(¯at)×   −(¯ωt)×       0          0          0       0   −I
         0      I   0   0   0   −(¯pt)× ¯Rt     0                         0             I      −(¯ωt)×       0          0       0     0
Art =    0     0   0   0   0  −  ¯dt × ¯Rt     0              Alt =      0          0          0      −(¯ωt)×       0       0     0
         0     0   0   0   0  −  ¯lt × ¯Rt     0                         0          0          0          0      −(¯ωt)×    0     0                                   0     0   0   0   0        0         0                                                                                                               0          0          0          0          0       0     0     
         0     0   0   0   0        0         0                         0          0          0          0          0       0     0
                                           T
ˆQ rt =  Ad¯Xt   015,6  Cov(wt)  Ad¯Xt   015,6                      ˆQ lt = Cov(wt)        06,15     I6              06,15     I6

Measurement                                Observation Matrix, H                        Observation Type

Forward Kinematic                            0   0  −I    I   0   0   0                   Right-Invariant
Relative Landmark Position                    0   0  −I   0    I   0   0                   Right-Invariant
Absolute Landmark Position                   (l)×   0  −I   0   0   0   0               Right-Invariant
Magnetometer                          (m)×   0   0   0   0   0   0                Right-Invariant
GPS Position                                 0   0    I   0   0   0   0                     Left-Invariant



                                          Table 3: Summary of Robo-centric State Estimator


State Deﬁnition                                   Deterministic Nonlinear Dynamics

     RBW   −BvB   BpBW   BpCW   BpLW             −(¯ωt)× Rt   −¯at −Rtg −(¯ωt)× vt   vt −(¯ωt)× pt   −(¯ωt)× dt   −(¯ωt)× lt 
       01×3    1      0      0      0                        01×3              0                 0            0           0
                                                                                    0                 0            0           0            Xt ≜  01×301×3    00      10      01      00         fut(¯Xt, ¯θt) =     01×301×3              0                 0            0           0
       01×3    0      0      0      1                        01×3              0                 0            0           0

Log-Linear Right-Invariant Dynamics                                       Log-Linear Left-Invariant Dynamics

    −(¯ωt)×       0          0          0          0         I   0         0     0   0   0   0        ¯Rt       0 
        −(¯at)×   −(¯ωt)×       0          0          0       0    I           (g)×   0   0   0   0    (¯vt)× ¯Rt    ¯Rt
           0             I      −(¯ωt)×       0          0       0   0              0      I   0   0   0    (¯pt)× ¯Rt    0
Art =      0          0          0      −(¯ωt)×       0       0   0     Alt =    0     0   0   0   0      ¯dt × ¯Rt    0
           0          0          0          0      −(¯ωt)×   0   0              0     0   0   0   0       ¯lt × ¯Rt    0                                        0          0          0          0          0       0   0                                                       0     0   0   0   0       0       0    
           0          0          0          0          0       0   0              0     0   0   0   0       0       0
                                                            "Ad¯X−1t     015,6 # Cov(wt) "Ad¯X−1t     015,6 #TˆQ rt = Cov(wt)                                                                                ˆQ lt =
                                                                                           06,15      I6               06,15      I6

Measurement                                Observation Matrix, H                        Observation Type

Forward Kinematic                            0   0    I  −I   0   0   0                   Left-Invariant
Relative Landmark Position                    0   0    I   0  −I   0   0                   Left-Invariant
Absolute Landmark Position                −(l)×   0    I   0   0   0   0               Left-Invariant
Magnetometer                       −(m)×   0   0   0   0   0   0              Left-Invariant
GPS Position                                 0   0  −I   0   0   0   0                  Right-Invariant





                                             33

<!-- PDF page 34 -->

Appendices

A.  Discretization of Filter Equations

In the preceding sections, the ﬁlters equations were in continuous time. However, in order to implement these ﬁlters
using software and physical sensors, these equations need to be discretized. For our implementation, we assumed a
zero-order hold on the inertial measurements, and performed analytical integration [34, 48]. In particular, analytical
integration was important for the resulting error dynamics to satisfy Theorem 2.

A.1.  World-centric Dynamics

This section demonstrates how to derive the deterministic, discrete time (world-centric) dynamics through analytical
integration of the continuous state (24) and bias (25) dynamics. The contact, landmark, and bias dynamics are simply
gaussian noise. Therefore, the discrete, deterministic dynamics are simply:
                                       ¯dtk+1 = ¯dtk,        ¯bgtk+1 = ¯bgtk,        ¯batk+1 = ¯b atk.                             (47)

Assuming a zero-order hold on the incoming IMU measurements between times tk and tk+1, the orientation can be
updated using the exponential map of SO(3):

                               Z tk+1
                                   ¯Rtk+1 =         ¯Rtk (¯ωt)× dt = ¯Rtk exp ¯ωtk∆t
                                                    tk

where ∆t ≜tk+1−tk. Integrating the velocity dynamics yields an equation that involves the integral of the exponential
map:
                       Z tk+1                          Z tk+1
                   ¯vtk+1 = ¯vtk +          ¯Rt¯at + g dt = ¯vtk + g∆t + ¯Rtk        exp  ¯ωtkt  dt   ¯atk.
                                       tk                                               tk
Likewise, analytically solving for the discrete position dynamics involves computing the double integral:

                                     1           Z tk+1 Z τ
                        ¯ptk+1 = ¯ptk + ¯vtk∆t + 2g∆t2 + ¯Rtk     tk      tk exp  ¯ωtkt  dt dτ   ¯atk.

To solve these integrals, it is useful to deﬁne an auxiliary function [15]:

                           ∞         !                                                  1
                            Γm(φ) ≜ X         (φ)n×    ,                                   (48)                                               (n + m)!
                                           n=0

which allows integrals to be easily expressed and computed using the taylor series form of the SO(3) exponential map.

             tk+1                   tk+1          ∞           !       Z               Z                         1           n
             exp (ωt) dt =       Γ0(¯ωtkt) dt = X          ¯ωtk∆t ×  ∆t = Γ1(ω∆t)∆t                                                 (n + 1)!             tk                        tk                 n=0
        tk+1   τ                         tk+1          ∞           !    Z    Z                 Z                          1           n
             exp  ¯ωtkt  dt dτ =       Γ1(¯ωtkt) t dt = X          ¯ωtk∆t ×  ∆t2 = Γ2(ω∆t)∆t2                                                       (n + 2)!        tk      tk                           tk                  n=0

Closed form expressions also exist, allowing fast and easy computation of these quantities [75].

                                      sin(||φ||)        1 −cos(||φ||)
                Γ0(φ) = I3 +        (φ)× +             (φ)2×                                           ||φ||                  ||φ||2
                             1 −cos(||φ||)          ||φ|| −sin(||φ||)
                Γ1(φ) = I3 +            (φ)× +                (φ)2×                            (49)                                            ||φ||2                     ||φ||3
                         1      ||φ|| −sin(||φ||)          ||φ||2 + 2 cos(||φ||) −2
                                                            ×                Γ2(φ) = 2I3 +       ||φ||3     (φ)× +          2||φ||4        (φ)2


                                              34

<!-- PDF page 35 -->

Remark 7. Γ0(φ) is simply the exponential map of SO(3), while Γ1(φ) is also known as the left Jacobian of SO(3)
[27, 6].

   Using these expressions, we can write down the discrete dynamics for the rotation, velocity, and positions states
as:
                             ¯Rk+1 = ¯Rk Γ0(¯ωk∆t)
                                 ¯vk+1 = ¯vk + ¯RkΓ1(¯ωk∆t)¯ak∆t + g∆t                                                                                                             (50)
                                                               1
                                ¯pk+1 = ¯pk + ¯vk∆t + ¯RkΓ2(¯ωk∆t)¯ak∆t2 + 2g∆t2,

where the t is dropped from the subscript for readability. These discrete dynamics are an exact integration of the
continuous-time system under the assumption that the IMU measurements are constant over ∆t.

A.2.  Covariance Propagation

In order to propagate the covariance, a continuous-time Riccati equation needs to be solved.

                                 d
                                                                                       t + ¯Qt                                     dtPt = AtPt + PtAT

The analytical solution to the differential equation above is given by [61]:

                                 Ptk+1 = Φ(tk+1, tk)PtkΦ(tk+1, tk)T + ¯Qd,                               (51)

where the discrete noise covariance matrix is computed by

                                Z tk+1
                                    ¯Qd =      Φ(tk+1, t)¯QtΦ(tk+1, t)Tdt,                                (52)
                                                     tk

and the state transition matrix, Φ(tk+1, tk), satisﬁes

                          d
                             dtΦ(t, tk) = AtΦ(t, tk) with Φ(tk, tk) = I.                              (53)

   The (world-centric) left-invariant error dynamics matrix only depends on the IMU inputs and the estimated bias
terms, see Table 2. Since both are assumed to be constant between times tk and tk+1, the state transition matrix can
be simply computed from the matrix exponential.

                                      Φl(tk+1, tk) = expm(Alt∆t)                                      (54)

This state transition matrix also has an analytical solution of the form:

                            Φl11   0    0    0   Φl15   0 
                                   Φl21  Φl22   0    0   Φl25  Φl26
                                   Φl31  Φl32  Φl33   0   Φl35  Φl36                          Φl(tk+1, tk) =                                                                 (55)
                                       0    0    0   Φl44   0    0
                                       0    0    0    0      I    0                                                                                                                                                                                                                                                                                                                                                                
                                       0    0    0    0    0      I

where the individual terms are

                            Φl11 = ΓT0 (¯ωk∆t)
                            Φl21 = −ΓT0 (¯ωk∆t) (Γ1(¯ωk∆t)¯ak)× ∆t
                            Φl31 = −ΓT0 (¯ωk∆t) (Γ2(¯ωk∆t)¯ak)× ∆t2


                                              35

<!-- PDF page 36 -->

                            Φl22 = ΓT0 (¯ωk∆t)
                            Φl32 = ΓT0 (¯ωk∆t)∆t
                            Φl33 = ΓT0 (¯ωk∆t)
                            Φl44 = ΓT0 (¯ωk∆t)
                            Φl15 = −ΓT0 (¯ωk∆t)Γ1(¯ωk∆t)∆t
                            Φl25 = ΓT0 (¯ωk∆t)Ψ1
                            Φl35 = ΓT0 (¯ωk∆t)Ψ2
                            Φl26 = −ΓT0 (¯ωk∆t)Γ1(¯ωk∆t)∆t
                            Φl36 = −ΓT0 (¯ωk∆t)Γ2(¯ωk∆t)∆t2.


The matrices Ψ1 and Ψ2 involve computing the solution to a more complicated integral. However, these integrals still
have analytical solutions which can be expressed easier after deﬁning φ ≜∥¯ωk∥and θ ≜φ∆t.

                          Z tk+1
                  Ψ1 ≜        (Γ0(¯ωkt)¯ak)× Γ1(¯ωkt) t dt
                                          tk
                  = (¯ak)× Γ2(−¯ωk∆t)∆t2
                                    sin(θ) −θ cos(θ)
                                                   (¯ωk)× (¯ak)×                                    φ3
                                   cos(2θ) −4 cos(θ) + 3
                   +                       (¯ωk)× (¯ak)× (¯ωk)×                                       4φ4
                               4 sin(θ) + sin(2θ) −4θ cos(θ) −2θ                                               (56)
                   +                                  (¯ωk)× (¯ak)× (¯ωk)2×                                             4φ5
                                   θ2 −2θ sin(θ) −2 cos(θ) + 2
                   +                               (¯ωk)2× (¯ak)×                                          2φ4
                                6θ −8 sin(θ) + sin(2θ)
                   +                         (¯ωk)2× (¯ak)× (¯ωk)×                                        4φ5
                                  2θ2 −4θ sin(θ) −cos(2θ) + 1
                   +                                (¯ωk)2× (¯ak)× (¯ωk)2×                                           4φ6

                       Z tk+1
               Ψ2 ≜       Γ0(¯ωkt)Φl25(t, tk) dt
                                     tk
               = (¯ak)× Γ3(−¯ωk∆t)∆t3
                          θ sin(θ) + 2 cos(θ) −2
                                                 (¯ωk)× (¯ak)×                                 φ4
                          6θ −8 sin(θ) + sin(2θ)
               +                        (¯ωk)× (¯ak)× (¯ωk)×                                  8φ5
                           2θ2 + 8θ sin(θ) + 16 cos(θ) + cos(2θ) −17                                              (57)
               +                                          (¯ωk)× (¯ak)× (¯ωk)2×                                          8φ6
                            θ3 + 6θ −12 sin(θ) + 6θ cos(θ)
               +                                  (¯ωk)2× (¯ak)×                                     6φ5
                           6θ2 + 16 cos(θ) −cos(2θ) −15
               +                                  (¯ωk)2× (¯ak)× (¯ωk)×                                     8φ6
                           4θ3 + 6θ −24 sin(θ) −3 sin(2θ) + 24θ cos(θ)
               +                                                (¯ωk)2× (¯ak)× (¯ωk)2×                                          24φ7
   The (world-centric) right-invariant error dynamics matrix depends on the the state estimates, ¯Rt, ¯vt, and ¯pt, which
will change between times tk and tk+1, see Table 2. Therefore, the state transition matrix will not simply be the matrix


                                              36

<!-- PDF page 37 -->

exponential, as in the left-invariant case. Solving (53) yields a state transition matrix of the form:
                                I    0   0  0  Φr15   0 
                                  Φr21    I   0  0  Φr25  Φr26
                                  Φr31  Φr32   I  0  Φr35  Φr36                            Φr(tk+1, tk) =                                                              (58)                                          0    0   0   I  Φr45   0
                                          0    0   0  0    I    0                                                                                                                                                                                                                                                                                                                                                     
                                          0    0   0  0   0      I

where the individual terms can be analytically computed as
                        Φr21 = (g)× ∆t
                                   1
                        Φr31 =  (g)× ∆t2                                   2
                        Φr32 = I∆t
                        Φr15 = −¯RkΓ1(¯ωk∆t)∆t
                        Φr25 = −  ¯vk+1 × ¯RkΓ1(¯ωk∆t)∆t + ¯RkΨ1
                        Φr35 = −  ¯pk+1 × ¯RkΓ1(¯ωk∆t)∆t + ¯RkΨ2
                        Φr45 = −  ¯dk+1 × ¯RkΓ1(¯ωk∆t)∆t
                        Φr26 = −¯RkΓ1(¯ωk∆t)∆t
                        Φr36 = −¯RkΓ2(¯ωk∆t)∆t2.


   Since the left/right-invariant errors are related through the adjoint, the two state transition and discrete noise ma-
trices also satisfy the following relations [8].
                               Φr = Ad¯Xk+1ΦlAd¯X−1k
                                                    r                     l                                                (59)
                                               ¯Q d = Ad¯Xk+1 ¯Q dAdT¯Xk+1

Therefore, the right-invariant state transition matrix can alternatively be computed using:
                              Φr(tk+1, tk) = Ad¯Xk+1 expm(Alt∆t) Ad¯X−1k  ,                              (60)

which can simplify implementation since many software libraries already contain efﬁcient methods to compute the
matrix exponential.
    Similar to the state transition matrices, the discrete noise covariance matrix (52) also has an analytical solution. In
practice, this matrix is often approximated as:
                                               ¯Qd ≈Φ ¯QkΦT∆t.                                           (61)

This approximated discrete noise matrix was used for all results in this article.

B.  Useful Lie Group Expressions

The matrix Lie group SEK(3) is known as the group of K direct isometries [8]. This group is comprised of a rotation
matrix, R ∈SO(3), and K vectors in R3, p1, · · · , pK. Let X be an element of SEK(3), which can be written as a
(3 + K) × (3 + K) matrix:
                              R   p1    · · ·  pK 
                                                     03,3   1     · · ·   0
                        X ≜                   ...                         ...     ...                    ...                                          (62)                                                                                                                                                          .
                                                     03,3   0     · · ·   1


                                              37

<!-- PDF page 38 -->

The group action is matrix multiplication. The adjoint is a linear map that can be used to move vectors between the
tangent spaces of two group elements. The matrix representation of the adjoint of SEK(3) is given by:

                               R     0    · · ·  0 
                                          (p1)× R  R    · · ·  0
                           AdX =                                ...                                    ...    ...                ...                                      (63)                                                                                                                                                               .
                                     (pK)× R  0    · · · R

The matrix representation of a vector, ξ ≜vec(φ, ξ1, · · · , ξK) ∈R3+3K, in the Lie algebra can obtained using the
“hat” operator:
                          (φ)×  ξ1    · · ·  ξK 
                                                03,3   0    · · ·   0
                    ξ∧=                                                                   (64)
                                                                                                                                                                                                                                      ...                            ...     ...                    ...                                                                                                                             ∈seK(3),
                                                03,3   0    · · ·   0
where (φ)× denotes the skew-symmetric matrix of a vector φ = vec(φ1, φ2, φ3) ∈R3 .

                              0   −φ3   φ2 
                             (φ)× ≜  φ3    0   −φ1 ∈so(3)                                 (65)
                               −φ2   φ1    0

The same vector can be moved to the Lie group through the exponential map:

                          Γ0(φ)  Γ1(φ)ξ1    · · ·  Γ1(φ)ξK 
                                                 03,3      1         · · ·     0
                            exp(ξ) =                          ...                                              ...         ...                                   ...                                   (66)                                                                                                                                                                          ,
                                                 03,3      0         · · ·     1

where Γ0(φ) is the exponential map of SO(3), and Γ1(φ) is the left Jacobian of SO(3).

C.  Error-state Conversions

Throughout this document, several versions of error states are used. These include the left/right invariant error (1),
the QEKF error states (21), and the “Euclidean orientation error” used for plotting the covariance hull (33). It is often
necessary to convert between these error states for plotting or when initializing the ﬁlters to provide fair comparisons.
For example, if the QEKF and the InEKF are initialized with identical covariance matrices, the underlying distribution
that they represent may be substantially different. This makes it impossible to show an accuracy comparison between
the InEKF and QEKF with identical initial uncertainty. This section provides details on how to convert between these
error states up to a ﬁrst-order approximation.
   When designing a QEKF, the orientation error can be deﬁned in either the local or global frame [75]. These errors
are equivalent to the left- and right-invariant errors for SO(3). In this document, the orientation error in the QEKF was
chosen to be the error deﬁned in the local frame (left-invariant error). Since the invariant errors are related through the
group’s adjoint, the exact relation between right-invariant and QEKF orientation errors is
                                     exp(ξRt ) = exp(¯Rtδθt).                                        (67)

When plotting the individual axes of the orientation error covariance hull, a “Euclidean orientation error” should be
used. Let δφt ≜φt −¯φt be this Euclidean error where exp(φ) ≜R is the exponential coordinate representation of
a particular orientation. When the errors are small, a ﬁrst-order approximation can be used to ﬁnd a mapping between
the right-invariant orientation error and this “Euclidean orientation error”.

                            exp(ξRt ) = ¯RtRTt = exp(¯φt) exp(−¯φt −δφ)
                                                                                                             (68)
                                   ≈exp(−Γ1(¯φt)δφ)


                                              38

<!-- PDF page 39 -->

A similar ﬁrst-order approximation can be used to ﬁnd the relation between the right-invariant error and the QEKF
velocity errors.

                             ηvt = ¯vt −¯RtRTt vt = ¯vt −exp(ξRt )vt
                                    ≈¯vt −vt − ξRt    vt = −δvt + (vt)× ξRt                            (69)
                                       ×
                 =⇒ξvt ≈−δvt + (¯vt)× ξRt

The same process can be repeated for the position states.

                                       ξpt ≈−δpt + (¯pt)× ξRt
                                                                                                             (70)
                                       ξdt ≈−δdt +  ¯dt × ξRt .

Acknowledgments

The authors would like to thank Yukai Gong for the development of the feedback controller utilized in the Cassie
experiments as well as Bruce Huang, Ray Zhang, Lu Gan, Zhenyu Gan, Omar Harib, Eva Mungai, and Grant Gibson
for their help in collecting experimental data. Funding for R. Hartley and M. Ghaffari is given by the Toyota Research
Institute (TRI), partly under award number N021515, however this article solely reﬂects the opinions and conclusions
of its authors and not TRI or any other Toyota entity. Funding for J. Grizzle was in part provided by TRI and in part
by NSF Award No. 1808051.

References

 [1] Nasradine Aghannan and Pierre Rouchon. On invariant asymptotic observers.  In IEEE Conf. Decision and
     Control, volume 2, pages 1479–1484. IEEE, 2002.

 [2] Brian DO Anderson and John B Moore. Optimal ﬁltering. Englewood Cliffs, 1979.

 [3] Yaakov Bar-Shalom, X Rong Li, and Thiagalingam Kirubarajan. Estimation with applications to tracking and
     navigation: theory algorithms and software. John Wiley & Sons, 2001.

 [4] Martin Barczyk and Alan F Lynch. Invariant extended Kalman ﬁlter design for a magnetometer-plus-GPS aided
      inertial navigation system.  In IEEE Conference on Decision and Control and European Control Conference
    (CDC-ECC), pages 5389–5394. IEEE, 2011.

 [5] Martin Barczyk and Alan F Lynch.  Invariant observer design for a helicopter UAV aided inertial navigation
     system. IEEE Transactions on Control Systems Technology, 21(3):791–806, 2013.

 [6] Timothy D Barfoot. State Estimation for Robotics. Cambridge University Press, 2017.

 [7] Timothy D Barfoot and Paul T Furgale. Associating uncertainty with three-dimensional poses for use in estima-
      tion problems. IEEE Transactions on Robotics, 30(3):679–693, 2014.

 [8] Axel Barrau. Non-linear state error based extended Kalman ﬁlters with applications to navigation. PhD thesis,
    Mines Paristech, 2015.

 [9] Axel Barrau and Silvere Bonnabel.  An ekf-slam algorithm with consistency properties.  arXiv preprint
     arXiv:1510.06263, 2015.

[10] Axel Barrau and Silvère Bonnabel. The invariant extended Kalman ﬁlter as a stable observer. IEEE Transactions
    on Automatic Control, 62(4):1797–1812, 2017.




                                              39

<!-- PDF page 40 -->

[11] Axel Barrau and Silvère Bonnabel.  Invariant Kalman ﬁltering. Annual Review of Control, Robotics, and Au-
    tonomous Systems, 2018.

[12] Axel Barrau and Silvère Bonnabel. Extended kalman ﬁltering with nonlinear equality constraints: a geometric
     approach. 2019.

[13] Billur Barshan and Hugh F Durrant-Whyte. Inertial navigation systems for mobile robots. IEEE Transactions
    on Robotics and Automation, 11(3):328–342, 1995. ISSN 1042-296X.

[14] Mehdi Benallegue and Florent Lamiraux. Estimation and stabilization of humanoid ﬂexibility deformation using
     only inertial measurement units and contact information. International Journal of Humanoid Robotics, 12(03):
     1550025, 2015.

[15] Michael Bloesch, Marco Hutter, Mark A Hoepﬂinger, Stefan Leutenegger, Christian Gehring, CD Remy, and
    Roland Siegwart. State estimation for legged robots: Consistent fusion of leg kinematics and imu. In Robotics:
     Science and Systems Conference (RSS 2012). RSS 2012: Robotics: Science and Systems Conference, 2012.

[16] Michael Bloesch, Christian Gehring, Péter Fankhauser, Marco Hutter, Mark A Hoepﬂinger, and Roland Siegwart.
     State estimation for legged robots on unstable and slippery terrain. In 2013 IEEE/RSJ International Conference
    on Intelligent Robots and Systems, pages 6058–6064. IEEE, 2013.

[17] Michael Andre Bloesch. State Estimation for Legged Robots–Kinematics, Inertial Sensing, and Computer Vision.
    PhD thesis, 2017.

[18] Silvere Bonnabel. Left-invariant extended Kalman ﬁlter and attitude estimation. In IEEE Conf. Decision and
     Control, pages 1027–1032. IEEE, 2007.

[19] Silvere Bonnabel. Symmetries in observer design: Review of some recent results and applications to ekf-based
     slam. In Robot Motion and Control 2011, pages 3–15. Springer, 2012.

[20] Silvere Bonnabel, Philippe Martin, and Pierre Rouchon.  Non-linear symmetry-preserving observers on Lie
     groups. IEEE Transactions on Automatic Control, 54(7):1709–1713, 2009.

[21] Silvère Bonnable, Philippe Martin, and Erwan Salaün. Invariant Extended Kalman Filter: theory and application
      to a velocity-aided attitude estimation problem. In Decision and Control, 2009 held jointly with the 2009 28th
     Chinese Control Conference. CDC/CCC 2009. Proceedings of the 48th IEEE Conference on, pages 1297–1304.
    IEEE, 2009. ISBN 1424438713.

[22] Guillaume Bourmaud, Rémi Mégret, Audrey Giremus, and Yannick Berthoumieu. Discrete extended Kalman
      ﬁlter on Lie groups.  In Signal Processing Conference (EUSIPCO), 2013 Proceedings of the 21st European,
     pages 1–5. IEEE, 2013. ISBN 0992862604.

[23] Guillaume Bourmaud, Rémi Mégret, Marc Arnaudon, and Audrey Giremus.  Continuous-discrete extended
    Kalman ﬁlter on matrix Lie groups using concentrated Gaussian distributions. Journal of Mathematical Imaging
    and Vision, 51(1):209–228, 2015. ISSN 0924-9907.

[24] Martin Brossard, Axel Barrau, and Silvere Bonnabel.  Rins-w: Robust inertial navigation system on wheels.
     arXiv preprint arXiv:1903.02210, 2019.

[25] Paul Chauchat, Axel Barrau, and Silvere Bonnabel. Kalman ﬁltering with a class of geometric state equality
      constraints. In 2017 IEEE 56th Annual Conference on Decision and Control (CDC), pages 2581–2586. IEEE,
     2017.

[26] Paul Chauchat, Axel Barrau, and Silvere Bonnabel.  Invariant smoothing on lie groups.  In 2018 IEEE/RSJ
     International Conference on Intelligent Robots and Systems (IROS), pages 1703–1710. IEEE, 2018.

[27] Gregory S Chirikjian. Stochastic Models, Information Theory, and Lie Groups, Volume 2: Analytic Methods and
    Modern Applications. Springer Science & Business Media, 2011.


                                              40

<!-- PDF page 41 -->

[28] Sachin Chitta, Paul Vemaza, Roman Geykhman, and Daniel D Lee.   Proprioceptive localilzatilon for a
     quadrupedal robot on known terrain.  In Robotics and Automation, 2007 IEEE International Conference on,
     pages 4582–4587. IEEE, 2007. ISBN 1424406021.

[29] Catherine Clifford. This start-up is building a humanoid robot that could soon be delivering packages to your
     door. May 2018. [Online; Published Tue, May 1 2018 1:05 PM EDT].

[30] Jose A Cobano, Joaquin Estremera, and P Gonzalez De Santos. Location of legged robots in outdoor environ-
     ments. Robotics and Autonomous Systems, 56(9):751–761, 2008. ISSN 0921-8890.

[31] Xingye Da, Omar Harib, Ross Hartley, Brent Grifﬁn, and Jessy W Grizzle. From 2D design of underactuated
     bipedal gaits to 3D implementation: Walking with speed tracking. IEEE Access, 4:3469–3478, 2016. ISSN
     2169-3536.

[32] Xingye Da, Ross Hartley, and Jessy W Grizzle. Supervised learning for stabilizing underactuated bipedal robot
     locomotion, with outdoor experiments on the wave ﬁeld. In Robotics and Automation (ICRA), 2017 IEEE Inter-
     national Conference on, pages 3476–3483. IEEE, 2017. ISBN 150904633X.

[33] James Diebel. Representing attitude: Euler angles, unit quaternions, and rotation vectors. Matrix, 58(15-16):
     1–35, 2006.

[34] Kevin Eckenhoff, Patrick Geneva, and Guoquan Huang. Closed-form preintegration methods for graph-based
      visual–inertial navigation. The International Journal of Robotics Research, page 0278364919835021, 2018.

[35] Jorhabib Eljaik, Naveen Kuppuswamy, and Francesco Nori. Multimodal sensor fusion for foot state estimation
      in bipedal robots using the extended kalman ﬁlter.  In Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., pages
     2698–2704. IEEE, 2015.

[36] Maurice F Fallon, Matthew Antone, Nicholas Roy, and Seth Teller. Drift-free humanoid state estimation fusing
     kinematic, inertial and lidar sensing. In IEEE-RAS Int. Conf. Humanoid Robots, pages 112–119. IEEE, 2014.

[37] P Fankhauser, M Bloesch, C Gehring, M Hutter, and R Siegwart. Robot-centric elevation mapping with uncer-
      tainty estimates. In International Conference on Climbing and Walking Robots, pages 433–440, 2014.

[38] C. Forster, L. Carlone, F. Dellaert, and D. Scaramuzza. On-manifold preintegration for real-time visual–inertial
     odometry. IEEE Trans. Robot., 33(1):1–21, 2017.

[39] Demoz Gebre-Egziabher, Roger C Hayward, and J David Powell. Design of multi-sensor attitude determination
     systems. IEEE Transactions on aerospace and electronic systems, 40(2):627–649, 2004. ISSN 0018-9251.

[40] Yukai Gong, Ross Hartley, Xingye Da, Ayonga Hereid, Omar Harib, Jiunn-Kai Huang, and Jessy Grizzle. Feed-
     back control of a cassie bipedal robot: Walking, standing, and riding a segway.  In 2019 American Control
     Conference (ACC), pages 4559–4566. IEEE, 2019.

[41] Mohinder S Grewal. Kalman ﬁltering.  In International Encyclopedia of Statistical Science, pages 705–708.
     Springer, 2011.

[42] JW Grizzle and Y Song. The extended Kalman ﬁlter as a local asymptotic observer for nonlinear discrete-time
     systems. Journal of Mathematical Systems, Estimation and Control, 5(1):59–78, 1995.

[43] Brian Hall. Lie groups, Lie algebras, and representations: an elementary introduction, volume 222. Springer,
     2015.

[44] Ross Hartley, Xingye Da, and Jessy W Grizzle. Stabilization of 3D underactuated biped robots: Using posture
     adjustment and gait libraries to reject velocity disturbances. In Control Technology and Applications (CCTA),
    2017 IEEE Conference on, pages 1262–1269. IEEE, 2017. ISBN 1509021825.



                                              41

<!-- PDF page 42 -->

[45] Ross Hartley, Maani Ghaffari Jadidi, Lu Gan, Jiunn-Kai Huang, Jessy W Grizzle, and Ryan M Eustice. Hy-
     brid contact preintegration for visual-inertial-contact state estimation using factor graphs.  In 2018 IEEE/RSJ
     International Conference on Intelligent Robots and Systems (IROS), pages 3783–3790. IEEE, 2018.

[46] Ross Hartley, Maani Ghaffari Jadidi, Jessy W Grizzle, and Ryan M Eustice. Contact-Aided Invariant Extended
    Kalman Filtering for Legged Robot State Estimation. In Proceedings of Robotics: Science and Systems, 2018.

[47] Jessica Kate Hodgins. Legged robots on rough terrain: experiments in adjusting step length, 1989.

[48] Zheng Huai and Guoquan Huang. Robocentric visual-inertial odometry. In 2018 IEEE/RSJ International Con-
     ference on Intelligent Robots and Systems (IROS), pages 6319–6326. IEEE, 2018.

[49] Guoquan P. Huang, Anastasios I. Mourikis, and Stergios I. Roumeliotis. Observability-based rules for designing
     consistent EKF SLAM estimators. The Int. J. Robot. Res., 29(5):502–528, 2010.

[50] Jemin Hwangbo, Carmine Dario Bellicoso, Péter Fankhauser, and Marco Huttery. Probabilistic foot contact esti-
     mation by fusing information from dynamics and differential/forward kinematics. In Intelligent Robots and Sys-
     tems (IROS), 2016 IEEE/RSJ International Conference on, pages 3872–3878. IEEE, 2016. ISBN 1509037624.

[51] Rudolph Emil Kalman. A new approach to linear ﬁltering and prediction problems. Journal of basic Engineering,
     82(1):35–45, 1960. ISSN 0021-9223.

[52] Arthur J Krener. The convergence of the extended Kalman ﬁlter. In Directions in mathematical systems theory
    and optimization, pages 173–182. Springer, 2003.

[53] Scott Kuindersma, Robin Deits, Maurice Fallon, Andrés Valenzuela, Hongkai Dai, Frank Permenter, Twan
     Koolen, Pat Marion, and Russ Tedrake. Optimization-based locomotion planning, estimation, and control design
      for the atlas humanoid robot. Autonomous Robots, 40(3):429–455, 2016.

[54] Ern J Lefferts, F Landis Markley, and Malcolm D Shuster. Kalman ﬁltering for spacecraft attitude estimation.
     Journal of Guidance, Control, and Dynamics, 5(5):417–429, 1982. ISSN 0731-5090.

[55] Pei-Chun Lin, Haldun Komsuoglu, and Daniel E Koditschek. A leg conﬁguration measurement system for full-
    body pose estimates in a hexapod robot. IEEE Transactions on robotics, 21(3):411–422, 2005. ISSN 1552-3098.

[56] Pei-Chun Lin, Haldun Komsuoglu, and Daniel E Koditschek. Sensor data fusion for body state estimation in a
    hexapod robot with dynamical gaits. IEEE Transactions on Robotics, 22(5):932–943, 2006. ISSN 1552-3098.

[57] Andrew W Long, Kevin C Wolfe, Michael J Mashner, and Gregory S Chirikjian. The banana distribution is
     gaussian: A localization study with exponential coordinates. Robotics: Science and Systems VIII, 265, 2013.

[58] Todd Lupton and Salah Sukkarieh. Visual-inertial-aided navigation for high-dynamic motion in built environ-
     ments without initial conditions. IEEE Trans. Robot., 28(1):61–76, 2012.

[59] Venkatesh Madyastha, Vishal Ravindra, Srinath Mallikarjunan, and Anup Goyal. Extended Kalman ﬁlter vs.
      error state Kalman ﬁlter for aircraft attitude estimation. In AIAA Guidance, Navigation, and Control Conference,
     page 6615, 2011.

[60] F Landis Markley.  Multiplicative vs. additive ﬁltering for spacecraft attitude determination.  Dynamics and
     Control of Systems and Structures in Space, (467-474), 2004.

[61] Peter S Maybeck. Stochastic models, estimation, and control, volume 3. Academic press, 1982.

[62] S J Merhav and M Koifman. Autonomously aided strapdown attitude reference system. Journal of guidance,
      control, and dynamics, 14(6):1164–1172, 1991. ISSN 0731-5090.

[63] J Murrell. Precision attitude determination for multimission spacecraft. In Guidance and Control Conference,
     page 1248, 1978.


                                              42

<!-- PDF page 43 -->

[64] Simona Nobili, Marco Camurri, Victor Barasuol, Michele Focchi, D Caldwell, Claudio Semini, and M F Fallon.
     Heterogeneous sensor fusion for accurate state estimation of dynamic legged robots. 2017. ISSN 0992374731.

[65] Simona Nobili, Marco Camurri, Victor Barasuol, Michele Focchi, Darwin G Caldwell, Claudio Semini, and
     Maurice Fallon. Heterogeneous sensor fusion for accurate state estimation of dynamic legged robots. In Robotics:
     Science and Systems, 2017.

[66] Tong Qin, Peiliang Li, and Shaojie Shen. Vins-mono: A robust and versatile monocular visual-inertial state
      estimator. IEEE Transactions on Robotics, 34(4):1004–1020, 2018.

[67] Gerald P Roston and Eric P Krotkov. Dead reckoning navigation for walking robots. Technical report, Carnegie-
    Mellon University, Pittsburgh, PA, Robotics Institute, 1991.

[68] Nicholas Rotella, Michael Bloesch, Ludovic Righetti, and Stefan Schaal. State estimation for a humanoid robot.
     In Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., pages 952–958. IEEE, 2014.

[69] Stergios I Roumeliotis, Gaurav S Sukhatme, and George A Bekey. Circumventing dynamic modeling: Evaluation
     of the error-state kalman ﬁlter applied to mobile robot localization. In Robotics and Automation, 1999. Proceed-
      ings. 1999 IEEE International Conference on, volume 2, pages 1656–1663. IEEE, 1999. ISBN 0780351800.

[70] Kenneth D Sebesta and Nicolas Boizot. A real-time adaptive high-gain ekf, applied to a quadcopter inertial
     navigation system. IEEE Transactions on Industrial Electronics, 61(1):495–503, 2014.

[71] Peyman Setoodeh, Alireza Khayatian, and Ebrahim Frajah. Attitude estimation by separate-bias Kalman ﬁlter-
     based data fusion. The Journal of Navigation, 57(2):261–273, 2004. ISSN 1469-7785.

[72] Surya PN Singh, Paul J Csonka, and Kenneth J Waldron.  Optical ﬂow aided motion estimation for legged
     locomotion. In 2006 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1738–1743.
    IEEE, 2006.

[73] Duncan Smith and Sameer Singh. Approaches to multisensor data fusion in target tracking: A survey. IEEE
     transactions on knowledge and data engineering, 18(12):1696–1710, 2006. ISSN 1041-4347.

[74] Randall Smith, Matthew Self, and Peter Cheeseman. Estimating uncertain spatial relationships in robotics. In
    Autonomous robot vehicles, pages 167–193. Springer, 1990.

[75] Joan Sola. Quaternion kinematics for the error-state Kalman ﬁlter. arXiv preprint arXiv:1711.02508, 2017.

[76] Yongkyu Song and Jessy W Grizzle. The extended Kalman ﬁlter as a local asymptotic observer for nonlinear
     discrete-time systems. In American Control Conference, pages 3365–3369. IEEE, 1992.

[77] Sebastian Thrun, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005. ISBN 0262303809.

[78] David Titterton, John L Weston, and John Weston. Strapdown inertial navigation technology, volume 17. IET,
     2004. ISBN 0863413587.

[79] Nikolas Trawny and Stergios I Roumeliotis. Indirect Kalman ﬁlter for 3D attitude estimation. Technical Report
     2005-002, Dept. of Computer Science & Engineering University of Minnesota, Minneapolis, MN 55455, 2005.
   URL http://mars.cs.umn.edu/tr/reports/Trawny05b.pdf.

[80] Yunfeng Wang and Gregory S Chirikjian. Error propagation on the Euclidean group with applications to manip-
      ulator kinematics. IEEE Transactions on Robotics, 22(4):591–602, 2006. ISSN 1552-3098.

[81] Yunfeng Wang and Gregory S Chirikjian. Nonparametric second-order theory of error propagation on motion
     groups. The International journal of robotics research, 27(11-12):1258–1273, 2008. ISSN 0278-3649.

[82] Oliver J Woodman. An introduction to inertial navigation. Technical report, 2007.



                                              43

<!-- PDF page 44 -->

[83] Kanzhi Wu, Teng Zhang, Daobilige Su, Shoudong Huang, and Gamini Dissanayake. An invariant-EKF VINS
     algorithm for improving consistency. In Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2017.

[84] X. Xinjilefu, Siyuan Feng, Weiwei Huang, and Christopher G. Atkeson. Decoupled state estimation for hu-
    manoids using full-body dynamics. Proceedings - IEEE International Conference on Robotics and Automation,
     2014. ISSN 10504729. doi: 10.1109/ICRA.2014.6906609.

[85] Zhenfei Yang and Shaojie Shen. Monocular visual–inertial state estimation with online initialization and camera–
   IMU extrinsic calibration. IEEE Transactions on Automation Science and Engineering, 14(1):39–51, 2017.

[86] Teng Zhang, Kanzhi Wu, Jingwei Song, Shoudong Huang, and Gamini Dissanayake. Convergence and consis-
     tency analysis for a 3-D invariant-EKF SLAM. IEEE Robotics and Automation Letters, 2(2):733–740, 2017.





                                              44