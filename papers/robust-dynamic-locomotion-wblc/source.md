# Extracted source text


<!-- PDF page 1 -->

        JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       1

     Robust Dynamic Locomotion via Reinforcement
       Learning and Novel Whole Body Controller

                           Donghyun Kim, Jaemin Lee, and Luis Sentis, Member, IEEE





          Abstract—We propose a robust dynamic walking controller   bipedal humanoid robots. A closely related work to ours, [2]
          consisting of a dynamic locomotion planner, a reinforcement   utilizes a trajectory parametrization of the dynamic locomotion
          learning process for robustness, and a novel whole-body locomo-                                                                       process [3], speciﬁcally customized for a particular robot, the
          tion controller (WBLC). Previous approaches specify either the
                                                    NAO. As such, our study can be viewed as a generalization of          position or the timing of steps, however, the proposed locomotion
         planner simultaneously computes both of these parameters as   this type of work to more general models typically used in the
         locomotion outputs. Our locomotion strategy relies on devising  dynamic walking communities [4] – e.g. inverted pendulums.2017
        a reinforcement learning (RL) approach for robust walking. The   In addition, the previous line of work on NAO robots, has
         learned policy generates multi step walking patterns, and the                                                                 remained quiet with respect to quantifying robustness. In the
         process  is quick enough to be suitable for real-time controls.
                                                           work presented here, we address robustness as a main thrust        For learning, we devise an RL strategy that uses a phase spaceAug         planner (PSP) and a linear inverted pendulum model to make the   performing detailed simulations with respect to unplanned and
7  problem tractable and very fast. Then, the learned policy is used   large disturbances at moderate walking speeds.
          to provide goal-based commands to the WBLC, which calculates     Since IP dynamics are in a reduced manifold, we propose
          the torque commands to be executed in full-humanoid robots.                                                                    a new type of whole-body controllers that are highly robust
        The WBLC combines multiple prioritized tasks and calculates
                                                               and  effective  to  transfer the IP-based locomotion process          the  associated  reaction  forces based on  practical  inequality
          constraints. The novel formulation includes efﬁcient calculation   into the full humanoid model. In particular we incorporate
          of the time derivatives of various Jacobians. This provides high-  new efﬁciently-computed feedforward terms, momentum and
          ﬁdelity dynamic control of fast motions. More speciﬁcally, we   balancing tasks, and more accurate contact models while main-[cs.RO]
        compute the time derivative of the Jacobian for various tasks                                                                            taining the key capability of task prioritization. In addition we
        and the Jacobian of the centroidal momentum task by utilizing
                                                                    completely reformulate the control structures for whole-body         Lie group operators and operational space dynamics respectively.
        The integration of RL-PSP and the WBLC provides highly   control with respect to previous work of ours on this area of
          robust,  versatile, and practical locomotion including steering   whole-body control. We accommodate for the new models and
         while walking and handling push disturbances of up to 520 N   also achieve high computational efﬁciency. As such, we build
         during an interval of 0.1 sec. Theoretical and numerical results                                                            on our long time history of devising whole-body controllers,
         are tested through a 3D physics-based simulation of the humanoid
                                                                                    this time around making signiﬁcant algorithmic changes. We         robot Valkyrie.
                                                                          believe these transformations constitute a quantum leap with
           Index Terms—Biped Locomotion, Reinforcement Learning,                                                                           respect to whole-body controllers with dynamic locomotion
        Whole Body Control
                                                                                  capabilities.
                                                            The combination  of RL-IP-PSP  for locomotion  pattern
                                        I. INTRODUCTION                       generation achieves signiﬁcant robustness by training a neural
                                                                 network through an actor-critic process with many possible       We explore the performance of a reinforcement learning
                                                                       center-of-mass states, representing potential disturbances, then        (RL) process and a new whole-body impedance and forcearXiv:1708.02205v1                                                                   learning successful step timing and foot position policies for          controller for robust dynamic locomotion on a full biped hu-
                                                                          recovery. Utilizing step timing and foot positions is not typ-        manoid dynamical model. Full-bodied 3D humanoid dynamic
                                                                                  ically explored because simultaneously varying both of these        walking based on inverted pendulum (IP) dynamics and RL
                                                                     parameters results in nonlinear system dynamics. [5] proposed         has not been studied to date. To enable the RL process to run
                                                                    a model predictive control (MPC) method for synthesizing          efﬁciently, we found that utilizing phase-space planning (PSP)
                                                                  walking patterns based on desired foot positions, kinematic          [1] provides a space of practical parameters that enables the
                                                                                    limits, and given step timing.  [6] formulated a nonlinear          transition function to operate in the reduced inverted pendulum
                                                                        optimization problem to solve two walking steps ahead of time         manifold. A key advantage of using an IP model is that  it
                                                                              to reduce computational cost. [7] linearized an optimization         generalizes locomotion for many types of systems with a light
                                                               problem by searching for a solution one step ahead of time.        dependency with their concrete kinematic structure. Using an
                                                                         In contrast, instead of relying on runtime optimizations, we         IP model not only reduces the search space but also enables the
                                                                                  train a control policy ofﬂine using an IP model, and use       same procedure to be used across different types of full-bodied
                                                                                                             it afterwards for real-time control of full humanoid robots
            D. Kim and J. Lee are with the Department of Mechanical Engineering,   being physically disturbed. Therefore, our learned locomotion
           University of Texas at Austin, Austin, TX, 78712 USA e-mail: .            planning generator can plan hundreds of steps ahead of time
             L. sentis is with the Department of Aerospace Engineering and Applied
          Mechanics, University of Texas at Austin, Austin, TX, 78712                in an instant, compared to the stepping time scale. As such,
             Manuscript received April 19, 2005; revised August 26, 2015.           speed is a key characteristic of the proposed planning and

<!-- PDF page 2 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       2





                                                                                   Fig. 2. PIPM and CoM phase plots. (a) PIPM 3D position moving on a
                                                                                   variable height surface. (b) Overlapped PIPM phase plots corresponding CoM
                                                                              paths during dynamic walking. In the sagittal plane, we can see multiple
                                                                              parabolas connected to each other corresponding to various walking steps.
                                                                             Parabolas in the frontal plane produce limit cycles.


Fig. 1. Type of humanoid platform our controller explores. The left image  WBC algorithms contain computations for Coriolis/centrifugal
shows NASA’s Valkyrie humanoid robot, with 135.9 kg weight and 1.83 m  and gravitational forces projected on in operational task space
height. The right image shows our dynamic simulation of Valkyrie using the
physics based simulator SrLib.                                           [14], [15], which are costly to calculate specially as the number
                                                               of control tasks increases. Our WBLC algorithms eliminates
                                                                         this problems. An analytic solution of the time derivatives of
control framework compared to the state of the art.            Jacobians is devised by employing Lie group operators, and
  Devising a new robust dynamic locomotion generator  is   an implementation using the Rigid Body Dynamic Library. We
insufﬁcient  to be  directly used  in  full humanoid  robots.   also eliminate the need to compute Coriolis/centrifugal terms
Therefore building on our expertise in this area, we devise   for every task priority.
a new type of whole-body controller (WBC) which we call     Overall, the main contributions of our study are as follows.
whole-body locomotion controller (WBLC) that focuses on   First, devising a novel learning framework for robust dynamic
speed, unilateral contact constraints, and speedy prioritized   locomotion under push disturbances achieving virtually in-
task control. The proposed WBC algorithm enables to efﬁ-   stantaneous re-planning of an order of magnitude more steps
ciently compute projection-based hierarchical task controllers   that the state-of-the-art. Second, we devise an elegant method
[8] and at the same time incorporate contact inequality con-   to introduce steering capabilities to phase-space planning for
straints which are represented by a quadratic programming   dynamically moving in all directions. Third, we devise a new
(QP) process [9]–[11], hierarchical quadratic programming   whole-body locomotion controllers, which yields the beneﬁts
(HQP)  [12]. While QP based  controllers have been very   of QP based computation of reaction forces and projection-
successful for ﬁeld application  their computational cost  is   based prioritized task control. Due to many optimizations, we
considerably higher than that of projection-based methods.   believe that this controller is one of the fastest WBC’s that
In contrast, projection-based methods have not incorporated   fulﬁlls both prioritization and practical inequality constraints.
before inequality constraints such as unilateral contact and   Lastly, we integrate all of these algorithms into a comprehen-
friction constraints. Our proposed WBC algorithm combines   sive software and conduct thorough testing on robust dynamic
for ﬁrst time QP and projection-based methods.               locomotion under large push disturbances on physics-based
  In our study, we introduce a centroidal angular momentum   simulations of Valkyrie.
(CAM) tasks to improve agile locomotion performance and    The paper is organized as follows. In Section II, we describe
we examine its effect when used in the whole-body control   the RL-IP-PSP process after brieﬂy reviewing related work
hierarchy. For example, when a robot quickly shakes or rotates   in Section C. We then introduce the formulation of WBLC
its body, we reduced undesirable arm movements that result   in Section III and the methods to efﬁciently obtain the time
from angular momentum compensation by introducing an arm   derivative of Jacobians for motion control and CAM tasks. In
motion task with higher priority than the CAM task.           Section V, we study the effects of our framework in agile task
  In the proposed WBLC, we devise new projection-based   such as shaking the robot’s body, walking while steering, and
recursive  structures  that incorporate  unilateral contact and   recovering from large pushes while walking. We do all of this
friction  constraints, yielding  the desired reduction on  the   using a model of NASA’s Valkyrie robot and the srLib physics
computational cost compared to other QP based algorithms.   based engine1(Fig.1). A more exhaustive review of previous
However, we don’t only achieve computational efﬁciency by  work can be found in Appendix C.
combining QP and projection-based methods. We do achieve
it by important improvements on the computation of the                II. REINFORCEMENT LEARNING BASED
projection-based operations themselves.                               PHASE SPACE PLANNER
  Indeed, in conventional projection-based methods, the com-
                                          We devise an RL process around a PSP framework, the latter
putational cost of some operations is considerably high. For
                                                                signiﬁcantly enhancing the learning efﬁciency by exploiting
instance, one well-known WBC algorithm  that uses  joint
acceleration, [13], includes costly terms such as the time      1Seoul National University Robotics Library. Physics-based simulation.
derivative of a null space projection matrix. In addition, many   Open-source http://robotics.snu.ac.kr/srlib/

<!-- PDF page 3 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       3


                                                    (a) Straight Walking     (b) Change the direction
                                                                                    {b}
                                                                 {a}





                                                                                 {b}
                                                                           {a}


                                                              {b}

                                                         {a}


Fig. 3. Phase Space Planner (PSP). (a) shows the method to ﬁnd a switching time and a lateral foot placement position given forward step location and an
apex velocity. In the sagittal phase plot, we can see the given current CoM state and the apex state uniquely deﬁne switching states     . From an initial state,
the planner computes the switching and apex times. These two timing values are used to ﬁnd the next step location in the lateral plane. (b) is the process
to steer the robot’s walking direction. When changing the walking direction, we ﬁrst align the orientation of the next local frame to the direction the robot
intends to go, and second we project the current CoM state into the next local frame.


the inherent directional walking constraints of PSP. PSP gener-  new frame. The original PSP algorithm devised locomotion
ates effective step switching information using simpliﬁed mod-   trajectories via numerical integration. However, for algorithmic
els such as the prismatic inverted pendulum model (PIPM). In   speed purposes, the methods presented here assume that the
Fig. 2, we show phase plots across multiple walking steps of  CoM height  is linear allowing us to exploit an analytical
the CoM sagittal and lateral phase portraits based on PIPM   solution (see Appendix. A).
dynamics. In the sagittal plane, the path consists of connected     Considering a one step ahead plan, an initial CoM state,
parabolas, while in the frontal plane, the walking path follows  and  desired  future  states  [px,  ˙xapex,  ˙yapex]⊤PSP ﬁnds
semi-periodic parabolas in a closed cycle. For convenience, we   the next step position and timing,  py,   tswitch ⊤. Notice
will use x for the sagittal plane and y for the frontal plane.     that the walking direction is indicated using apex velocities,
                                                                                               [˙xapex,  ˙yapex]⊤. We will now see that our formulation of
A. Phase Space Planner                             PSP makes the RL problem more efﬁcient by reducing the
  Leading step planning generators, such as Divergent Com-   dimensionality of the learned state variables.
ponent of Motion [16], ﬁnd CoM paths given step positions
and  their timing as input information. The ZMP Preview
Control method [17] has different mechanics but the generated   B. The Reinforcement Learning Problem
output can be interpreted as ﬁnding the CoM path given step
                                                 As mentioned before, a central part of our walking method-position and timing input information. In contrast, PSP ﬁnds
                                                          ology is to achieve robustness via reinforcement learning. Thethe step switching time and lateral foot positions, given sagittal
                                                             technique we use is the Actor-Critic with Eligibility Tracesfoot positions and apex velocities (Fig. 3). The apex states are
                                                         method. We summarize this process in Algorithm 1 which isthose at the instant when the sagittal CoM velocity is at its
                                                        an adaptation [18]. We deﬁne s, as CoM apex states, s ≜minimum; equivalently, they can be considered as states where
the sagittal CoM position is zero in a local frame attached to    yapex,   ˙xapex,   ˙yapex ⊤. Notice that s does not include the
the stance foot, i.e. below the CoM sagittal position.            variable xapex because it is assumed to be always zero in the
  In Fig. 3(a), we can see that the current robot’s CoM state   local frame. We deﬁne actions, a ≜  px,   ˙xapex,   ˙yapex ⊤,
and the next desired apex state uniquely deﬁne a switching   as input parameters to the PSP process. A transition function,
state     , a switching time, and an apex time. These timings   T(s, a), computes the next apex state, s′, and the instanta-
are used to ﬁnd the next  lateral foot position, py,2. Note   neous reward value. In Fig. 4, we show the transition function,
that the resultant locomotion trajectory is straight forward if   consisting of two stages: 1) ﬁnding step timing and position
˙xapex is a positive number and ˙yapex = 0. In contrast, the   values via PSP, and 2) computing the next apex state via
proposed algorithm, applies a simple and elegant modiﬁcation   an analytic solution of the linear inverted pendulum model
that allows to dynamically steer the biped in any direction   (LIPM). The ﬁrst stage is described in Appendix A and allows
of walking (see Fig. 3(b)). When we need to turn walking   to ﬁnd tswitch, tapex, and py from the current apex state and
direction, we re-initialize the orientation of the local frame   chosen action. The second stage, ﬁnds the next apex state using
{b} to the new direction and project the current state to the   the analytic solution of the CoM dynamics (see Eq. (35)). In

<!-- PDF page 4 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       4


 Algorithm 1: Actor-Critic with Eligibility Traces
  Input: ˆv(s, w), ∀s ∈S, w ∈R18×30×56+1                                                                                                                          min      max
  Input: π(a|s, θ), ∀a ∈A, s ∈S, θ ∈R(18×30×56+1)×6
                                                                                                                                                               weighted                                                                                                                                                                                                                    ......    connections                                         min      max  Result: θ, w
   Initialize policy weights θ and state-value weights w                  Input layer                                                                                       Action
                                                                                                                                                                                        Bias                                                        min      max
   while (variances of policy is large) do                                                                             node                  Output layer                           Truncated
     Randomly pick s in S                                                                      Hiddenradial basislayerfunctionof Gaussiannodes                                          normal distribution
     eθ ←0 (eligibility trace of policy parameters)
    ew ←0 (eligibility trace of value parameters)               Fig. 5.   Radial Basis Function Neural Network for Walking Policy
                                                                          Representation. Outputs of the neural network are means and standard
      I ←1                                                                 deviations of each action value. The truncated normal distributions deﬁned
      while (s is not terminal) do                               by the outputs are used to stochastically pick actions.
       a ∼π(·|s, θ)
            s′, R ←T(s, a)                                                                     Fig. 5 shows that outputs of the RBF network are means
         δ ←R + γˆv(s′, w) −ˆv(s, w)                                                       and standard deviations of truncated normal  distributions,
       ew ←λwew + I∇wˆv(s, w)                         π(a|s, θ). The range of  the  distributions  are  selected by
        eθ ←λθeθ + I∇θ log π(a|s, θ)                      considering the desired walking speed and step length limits
     w ←w + βδew                                                               as follows:
       θ ←θ + αδeθ
                                                                                                                    · 0.1 ≤px ≤0.5 (m),         I ←γI
         s ←s′                                                                                            · 0.03 ≤˙xapex ≤0.37 (m/s),               (2)     end
  end                                                                                                           · −0.25 ≤˙yapex ≤0.25 (m/s).

                                                   The network’s outputs are linearly weighted by θ; thus, the
                                                          purpose of RL is to ﬁnd the weights θ given candidate actions
                                                                      that minimized the desired cost.
                                                     The instantaneous reward is deﬁned by the forward velocity
                                                                    error and lateral step size error:                    Phase               Linear
                    Space               Inverted
                                   R = −(˙xnomapex −˙xapex)2 −15×(pnomy   −py)2 −(˙yapex)2. (3)                      Planner           Pendulum

                                                   The set target for the learning process is to achieve recovery
                                                             behaviors that maintain a straight forward direction, ˙yapex =
Fig. 4.  Transition Function. The transition function relies on two models:
PSP and LIPM. Given an apex state and a considered action, PSP computes  0 while keeping a nominal lateral directional step size. We
step timing and location information that serve as inputs to the LIPM model.   choose ˙xnomapex = 0.2m/s and pnomy  = 0.3m. The reward comes
Then, LIPM solves for the next apex state based on the given state and the  from the transition function described before, given current
provided inputs.
                                                        apex and action states selected from the truncated distributions.
                                                                                  If the next predicted apex state incurs a terminal condition,
                                                                 the transition function gives a negative reward of −5.0, andAlgorithm 2 the process of ﬁnding the switching times and
                                                                 the process terminates and starts a new iteration. The set ofthe next apex states is explained in detail.
                                                                  safe conditions (i.e. opposite to the terminal conditions) is the
  The next item, ˆv(s, w), corresponds to the value function -
                                                                    intersection of the following predicates:
similar to the cost-to-go function in Dynamic Programming.
We store its learned values using a radial basis function (RBF)                                 · tapex > 0.12 (s),
neural network [19]. The network uses a three-dimensional
                                                                                                                            · tswitch > 0.12 (s),                   (4)input vector consisting of the CoM apex state.
                                                                                                                            · 0.1 < py < 0.5 (m),
                     · −0.14 ≤yapex ≤0.2 (m),
                                                      which reﬂect the ability of the robot to swing its legs and the
                     ·   0.03 ≤˙xapex ≤0.61 (m/s),             (1)                                                                          lateral step length. Notice that we do not include a predicate
                     · −0.55 ≤˙yapex ≤0.55 (m/s).               about the sagittal step length because it is already bounded by
                                                                 the allowable action range. The learning process ends when the
The hidden layer consists of a bias term and 18 × 30 × 56   variance of the learned policy becomes small enough (< 0.07
Gaussian functions with centers on a grid with 2cm spacing   units in our case). The usual number of iterations required to
along each input dimension. The policy function also consists   complete the learning process is about 30,000, and the process
of an RBF neural network but a little different from the value   usually takes about 1 min to compute on a dual-core, 3.0
function because of actions are chosen based on an stochastic  GHz, Intel i7 processor thanks to the speed of our analytic
evaluation.                                        PSP method.

<!-- PDF page 5 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       5


C. Evaluation of Learned Policy                                                               2 iter     CoM5000pathiter           Step position             (0.05, 0.39,Post0.33)impulse state(0.06, 0.24, -0.06)
   Fig. 6 shows that the performance of the RL-based planner                3000 iter          Final                                               (0.05, 0.26, 0.04)      (0.06, 0.20, -0.07)
increases as the number of iterations increases. By watching
the posture of a robot at different CoM states, we choose
the nominal apex  state  to be  yapex,   ˙xapex,   ˙yapex  =
[ 0.056,  0.2, 0 ]⊤. We proceed by simulating push  dis-
turbances to the CoM based on various external forces and
directions. We use mean values of the ﬁnal learned policy
as desired actions rather than randomly picking actions from
the normal  distributions. The  results are shown in Fig. 6
showing the learned policy obtained after many iterations and
their enhancements on the walking patterns. In this ﬁgure,
                                                                                                                         (a) push outward
initially our simulated robot stands with the right foot on the
ground and we simulate push disturbances to the left, right,
and forward directions of its body. For example, the    post
impulse apex state, [ 0.05, 0.39, 0.33 ]⊤, is the result of an
impulse applied to the left-forward direction of the robot’s
body. Red lines are interrupted within a few walking step
indicating that the initial policies fail to ﬁnd proper actions.
In contrast, pink lines correspond to the ﬁnal learned policy
which achieves inﬁnite walking steps without falling given the
initial push disturbances.


         III. WHOLE BODY LOCOMOTION CONTROL                                                (b) push inward
  We devise a new whole-body locomotion control algorithm,
                                                                                   Fig. 6. Phase Plots of Sequential Steps from Learned policies. The initial
dubbed WBLC, that speciﬁes tasks using a hierarchy of accel-    state considered here corresponds to an impulsive disturbance. The candidate
erations and uses quadratic programming to determine contact   phase trajectories generated by the policy function reach terminal states if
forces. Fig. 7 describes the overall process for computing the    they are unsuccesful. As learning proceeds, the policy function ﬁnds better
                                                                                  actions which avoid terminal states. The ﬁnal policy achieves inﬁnite number
torque commands. The details are described below.                of steps without reaching terminal conditions.


A. Acceleration-based Formula with Hierarchy
                                                            Jacobian associated with the ﬁrst task, J1. The Equation (8)  Task level controllers are computed in operational space as
                                                         can be extended to the general n task case, using the followingacceleration commands and converted to joint accelerations
                                                               hierarchyusing differential forward kinematics,

                           ˙x1 = J1 ˙q,                                                     n
                                                              (5)                                                                                                 ¨q[task] = J1¨ed1 + X ¨qk,  (n ≥2)          (9)                           ¨x1 = J1¨q + ˙J1 ˙q,
                                                                                k=2
where x ∈Rn and q ∈Rm represent the task’s operational
coordinate and the joint positions, respectively, and J is the                                                           with
corresponding Jacobian matrix. Then, the joint acceleration for
a desired task acceleration, ¨xd1 can be resolved as                                      k−1 !
                                                                                  ¨qk = Jk|prec(k)   ¨edk −Jk X ¨qi    ,
                   ¨q1 = J1  ¨xd1 −˙J1 ˙q = J1¨ed1,             (6)                                i=1
                                                                        Jk|prec(k) = JkNprec(k),
where J1 indicates the dynamically consistent inverse of J1,                                                           (10)
i.e.                                                                 k−1
                                  −1                     Nprec(k) = Y Ns|s−1  (k ≥2,  N1|0 = N1),           J1 = A−1J⊤1  J1A−1J⊤1       ,             (7)
                                                                       s=1
where A ∈Rm×m indicates the mass/inertia matrix of the      Ns|s−1 = I −Js|prec(s)Js|prec(s)  (s ≥2).
rigid body model of the robot. If we consider now the mapping
of two operational tasks ¨xd1 and ¨xd2, we propose the following   This task hierarchy  is similar, albeit not identical to [13].
task hierarchy mapping                                Compared to  it, our proposed method is more concise, re-
                                                                    sulting in less computations for similar control speciﬁcations.                    ¨q = J1¨ed1 + J2|1  ¨ed2 −J2¨q1  ,             (8)
                                                               In  particular we do not require the computation of time
where J2|1 ≜(J2N1) represents the Jacobian associated with   derivatives of prioritized Jacobians. Details on the similarities
the second task, J2, projected into the null space of the ﬁrst  and differences between these two works are discussed in
task, N1 = I −J1J1, which by deﬁnition is orthogonal to the  Appendix B.

<!-- PDF page 6 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       6


                                                                  task than body rotational tasks as we will soon see. In addition,
                                                        sometimes it is not possible to simultaneously fulﬁll linear and
                                                              angular momentum speciﬁcations. For that reason, we speciﬁc
                                       CoM behavior as a hard constraint while relaxing angular
                                                                behavior, i.e.
                                                        min F⊤r QFr + ∥Fdcm,ang −WangFr∥2
                                                                      Fr

                                                                  Subject to.  µ|Fr,z| ≥|Fr,x|                       (14)
                                                                                µ|Fr,z| ≥|Fr,y|
                                                           Fdcm,lin −WlinFr = 0
                                                      where Fdcm,lin and Fdcm,ang are the desired linear and angular
                                                                    parts of the CM, µ represents a friction coefﬁcient related to
                                                                 the contact surfaces, Q is a weighting matrix, and Wang and
                                                  Wlin are mappings from reaction forces to angular and linear
                                                  momenta behaviors. Based on the results of this optimization,
                                                        Fr, the desired value of the CAM task can be calculated as
                                                                 follows:
                                                                 Icm¨xdcm = Fdcm =  Fdcm,lin  WangFr  ⊤,      (15)

                                                      where Icm  is a spatial inertial term. Notice that the term
                                            WangFr might be different than Fdcm,ang since the desired
                                                              angular behavior might violate friction cone constraints. From
                                                                 the above equation, we extract the desired CM acceleration
                                               command ¨xdcm for usage in the controller hierarchy. MoreFig. 7.  Block Diagram of the Proposed Whole-Body Locomotion Con-
troller. In WBLC, motion commands are compounded as joint accelerations   concretely, ¨xdcm =  ¨xdCoM αdang  , where the ﬁrst term within
based on null-space projection methods. The CM task speciﬁcation is usd to   the parenthesis is the desired CoM acceleration and the sec-
compute reaction forces via QP optimization including unilateral contacts and
                                                     ond term is the desired angular acceleration. Both of thesefriction cone constraints. The computed joint acceleration and reaction forces
are used to sove for torque commands, which are the ﬁnal output of WBLC.  commands are used separately in the hierarchy deﬁned in Eq.
                                                                           (9), to produce the joint acceleration command ¨q[task] which
                                                                    in turn yields ¨qd via Eq. (12). Plugging this last term into
B. Optimizing Reaction Forces of Underactuated Robots                                                          Eq. (11) we obtain
  Based on the desired joint acceleration given in (Eq. (9)),
                               A  ¨q[task] + Nn|prec(n)¨qres +b+g+J⊤r Fr = U ⊤τ, (16)WBLC ﬁnds torque commands via the following equation:
                                                      which can be written in matrix form as
       A(q)¨qd + b(q, ˙q) + g(q) + J⊤r Fr = U ⊤τ,    (11)
                                                 ⊤                   τ
where q ∈Rn+6 and b(q, ˙q) and g(q) are the joint space      U    −ANn|prec(n)      ¨qres  = τ[task],      (17)
coriolis/centrifugal and gravity terms, respectively. Fr and Jr
                                                      where we have deﬁned the termrepresent the reaction forces and the corresponding contact
Jacobian. τ ∈Rn and U ⊤∈R(n+6)×(n)  represent the                 τ[task] ≜A¨q[task] + b + g + J⊤r Fr.        (18)
actuator torque commands and the selection matrix mapping
actuated torque to the ﬂoating base dynamics. Note that ¨qd is  We now have an underdetermined matrix system which can
chosen as,                                               be solved via pseudo inversion as
                  ¨qd = ¨q[task] + Nn|prec(n)¨qres,           (12)          τ        ⊤             +                                          = U    −ANn|prec(n)     τ[task]     (19)
                                                                                     ¨qreswith
              Nn|prec(n) = Nprec(n)Nn|n−1           (13)  where (.)+ represents the Moore-Penrose pseudo inverse op-
                                                                      eration.where ¨qres is a residual joint acceleration command.
  To ﬁnd the reaction forces Fr, we specify a centroidal
                                                                         IV. TIME DERIVATIVE OF JACOBIANmomentum (CM) operational task. A CM task consists of
linear and angular momenta portions. The linear part, corre-    The ability to compute efﬁciently the time derivative of
sponds to the robot’s CoM behavior, Fcm,lin, and is typically   Jacobian operators for fast operational space control has been
used for locomotion planning. On the other hand, the angular   overlooked. However it plays an important role on robustifying
behavior, the so-called CAM, Fcm,ang, is typically set to zero   fast movements. Fig.8 shows that the tracking performance of
value. Setting the angular task to zero creates conﬂict with   a simple serial manipulator is signiﬁcantly enhanced by using
other tasks, such as body rotational tasks. We circumvent this   the term ˙J ˙q via Operational Space Control (OPC), where J
problem by projecting angular behavior as a lower priority    is the Jacobian of the end effector and ˙q is the vector of joint

<!-- PDF page 7 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       7





     0.2                                                            0.2


     0.1                                                            0.1

      0                                                   0

    -0.1
                                                                      -0.1

    -0.2
                                                                      -0.2

    -0.3
                                                                      -0.3
          0     0.1    0.2    0.3    0.4    0.5    0.6                                                             0      0.1     0.2     0.3     0.4     0.5     0.6      Fig. 9.  Multi-DoF Openchain. The openchain consists of n joints. At the
                                                                     end of the chain, the end-effector is attached to link n.


Fig. 8.  Tracking performance comparison with and without the term
˙J ˙q. A three-DoF planar manipulator is used to control its end effector to
follow a vertical line (red lines) with 2 Hz frequency (blue dashed lines are   frame associated with Vi can be obtained via adjoint deriva-
the end-effector path). The tracking results demonstrte that the (a) controller,   tions,
which accounts for ˙J ˙q, outperforms the (b) controller.

velocities. Notice that ˙J is used in our WBLC in Equation (6).                 AdTg,i (Vi) = Tg,iViTg,i−1
The commanded task is to follow a vertical line deﬁned by                = Tg,iTg,i−1 ˙Tg,iTg,i−1           (24)
the function, xd = [ 0.62, 0.23 sin(4πt) ]⊤. The OPC input                               −1                                                = ˙Tg,iTg,i .is

            0
  ¨x =           + Kp(xd −x) + Kv(˙xd −˙x). (20)  The adjoint mapping operator is deﬁned as      −36.32 sin(4πt)

We will use Lie group theory to compute the derivatives of                               Ri,j      0
                                                                            AdTi,j ≜                                ,           (25)point task Jacobians [20]. We implement this functionality                             [pi,j]×Ri,j   Ri,j
using the Rigid Body Dynamics Library 2, which is a popular
open source dynamics toolbox. In addition, we also devise a  where Ri,j and pi,j are relative rotations and positions be-
new method to compute the time derivative of the CM Jacobian   tween points i and j. The generalized velocity of point p in
which cannot be computed using Lie group theory.              local coordinates (see Fig. 9) can be represented as

A. Time Derivative of Point Jacobian                         Vp = AdTp,nVn
  Lie group operators provide convenient analytic deriva-          = AdTp,n−1Vn−1 + AdTp,nSn ˙qn
tions for Jacobian computations. The SE(3) orientation and                                                                                                                 ...                                    (26)position representation of a rigid body in three-dimensional
space consists of orientation matrix (R) and a position vector                              n
                                          = AdTp,0V0 + X AdTp,iSi ˙qi.(p). It can also be represented via the 4 × 4 homogeneous
transformation,                                                                             i=1

                          Rg,i   pg,i
                                                              ,              (21)                   Tg,i =                                                          Because {0} frame is the global frame (an inertial frame),                         0    1
                                          V0 is equal to zero. On the other hand Si maps joint velocities
where, Rg,i and pg,i represent the orientation and position   to R6, e.g. Si  is  [ 0, 0, 1, 0, 0, 0 ]T means  ˙qi  is a revolute
of  the  ith frame  in  global  coordinates  respectively (See                                                                        joint rotating along the z local axis. The ﬁrst three positions
Fig. 9). The velocity representation in se(3) consists of the 6-                                                               of Si represent rotational axes while the last three positions
dimensional vector, [w, v]T , and yields the 4×4 homogeneous                                                                 represent prismatic axes. It can be shown that the Jacobian of
equality,                                                           a point p, is equal to
                        [wi]×  vi
                 Vi ≜                         ,               (22)                         0    0
                                                       Jp = AdTp,1S1  AdTp,2S2    · · ·  AdTp,nSn      (27)
where
                0    −wi,3    wi,2 
                                                         (23)                         wi,3     0    −wi,1           [wi]× ≜                                       Furthermore, let’s break down the adjoint operators into the                                                                                          following chain operation                    −wi,2    wi,1     0

Here, wi,1, wi,2, wi,3 are relative angular velocities along the
                                                                    AdTp,iSi = AdTp,p′AdTp′,nAdTn,iSi.        (28)three Cartesian axes, and vi is the linear velocity. It can be
shown that Vi = Tg,i−1 ˙Tg,i, and corresponds to the generalized
velocity seen from the ith frame. The velocity in the global  Here p′ is a virtual point representing the position of p but with
                                                                    local orientation with respect to frame n. As such it represents
  2Open-source https://rbdl.bitbucket.io                                     just a position offset. In this case Tp′,n is constant and the i-th

<!-- PDF page 8 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       8



                                                                          (1)                         (2)      (3)
                 Whole body Motion with Hierarchy Set 1                    1.2                                                                               350
                                                                                                                                                                                     Desired Value
                                                                                                                                          Peak Point in
                                                                 1                                                                                                                    Hierarchy Set 1
                                                                                                                                                      Hierarchy Set 2
                                                                                                                                                                                     Hierarchy Set 2
                                                                                0.8                                                                                300

                                                                                0.2
                                                                 0                                                                                                                                         (Nm)
                                                                                                                                                  250       Initial Pose         Pose at (1)          Pose at (2)           Pose at (3)                          orientation                                                                                     -0.2                                                                                                                                                                                                                                            torques                                                                                                            body                                                                                0.2                                                                                Peak Point in
                                                      of                                                                                                                                                                                joint 200     Hierarchy Set 1                 Whole body Motion with Hierarchy Set 2
                                                                 0                                                                    of
                                                                                     -0.2                                                                                                                                       Norm                                                                                                                                                                                                                                                                             Quaternion
                                                                                0.2                                                                                150


                                                                 0

       Initial Pose         Pose at (1)          Pose at (2)           Pose at (3)          -0.2 3       3.2       3.4       3.6       3.8      4       4.2       4.4      4.6      4.8      5   1003    3.2   3.4   3.6   3.8   4    4.2   4.4   4.6   4.8   5
                                                                                        Time (sec)                                               Time (sec)
                             (a)                                                                    (b)                                                               (c)


Fig. 10. Body shaking test using different task hierarchies: Whole body movements generated via WBLC change corresponding on the task hiearchy.
(a) contains simulations using two task hierarchy sets (b) shows data of quaternion tracking error for a body orientation task (c) shows the norm torques
generated by WBLC in each case


column of the time derivative of the Jacobian can be resolved                         V. RESULTS
as                                                     To verify the performance of the proposed methods, we
                     ˙                                             conduct  three demonstrations: 1) body  orientation  control
  ˙Jp,i = z AdTp,iSi}|   {                                        while changing the task hierarchy, 2) dynamic locomotion
                     ˙                                              with directional change, and 3) push-recovery from various
        z   }|   {     n     o                                              directions while walking. Toward these  investigations, we   =  AdTp,p′  AdTp′,nAdTn,iSi
                                                        implement our algorithms on a simulation of the Valkyrie
                                               ˙
                        z    }|    {                     humanoid robot, and test it using the physics based simulation
     + AdTp,p′AdTp′,n AdTn,iSi                           SrLib. Because our focus is on locomotion, we ﬁx the ﬁnger
   = AdTp,p′adVp,p′AdTp′,nAdTn,iSi                    and wrist joints, bringing the total number of joints to 28. To
                 n                  o     incorporate ﬂoating body dynamics, prismatic and ball joints     + AdTp,p′AdTp′,n  AdTn,iadVn,iSi + AdTn,i(˙Si)                                                                 are introduced to connect Valkyrie’s pelvis to a ﬁxed frame.
                                                         (29)                                                                  In the simulation environment, we use a friction coefﬁcient
                                                       between the ground and the robot’s feet of 0.8. On the other
  Here we have used AdT˙  = AdT (adV ) and since V =  hand the  friction cone constraints used in WBLC are  set
T −1 ˙T , then we deﬁne adT −1 ˙T ≜T −1 ˙T −˙T T −1.             to a value of 0.65 to be conservative. In case our contact
                                                                 control solver fails to ﬁnd proper reaction forces, we allow
                                                                    for solutions that violate friction constraints by relaxing the
B. Time Derivative of the Centroidal Momentum Jacobian                                                                        friction coefﬁcient to a value of 1.75. The resulting control
  The previous equations for the time derivative of point   solution implies that slip occurs but only for very short times
Jacobians are not applicable to the CM Jacobian. The latter   (in general less than 0.005 s). This simple technique doesn’t
can be obtained from the CM task deﬁnition of Eq. (15)   incur an increase in computational complexity while greatly
linear part  is simply the weighted sum of time derivatives   enhancing the robustness of WBLC with respect to external
of each link’s CoM Jacobian. However, the angular part is   disturbances.
not  straightforward. Instead of ﬁnding  ˙Jcm, we can ﬁnd
the multiplication of ˙Jcm and the  joint  velocities,  ˙q, via                                                             A. Body Orientation Control with Various Task Hierarchies
operational space dynamics:
                                                   Body shaking behavior  is a  difﬁcult  skill  that we use
         Λcm(q)¨x + µcm(q, ˙q) + pcm(q) = Fr,      (30)   here to study the dynamic performance of WBLC tasks. In
                                                                       traditional humanoid control methods, CoM and CAM tasks
Here, Λcm, µcm, and pcm are an inertia matrix, coriolis and   are controlled within the same priority  level. We propose
centrifugal force, and gravitational force of the CM operational   to split them via WBLC into different hierarchy levels. To
task, respectively. Since there is no coriolis and centrifugal   demonstrate this feature, we deﬁne the following six tasks:
effects in CM space, µcm is zero. Thus, ˙Jcm ˙q must be equal        ·  ¨x1 ∈R3: Linear CoM
to JcmA−1b:                                                                              ·  ¨x2 ∈R3: Centroidal Angular Momentum (CAM)
                    ˙Jcm ˙q = JcmA−1b.                (31)        ·  ¨x3 ∈R3: Body Orientation
                                                                                                   ·  ¨x4 ∈R22: Partial Joint Posture (all joints except shoulder
All terms in JcmA−1b are easily computable usingoff-the-         pitch, shoulder roll, and knee pitch)
shelf dynamics libraries.                                                               ·  ¨x5 ∈R3: Pelvis Orientation

<!-- PDF page 9 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                       9


    ·  ¨x6 ∈R28: Full Joint Posture
Most tasks above are self-explanatory. We introduce a partial
joint posture consisting on keeping the initial joint positions
for  all robot joints except for the shoulder pitch and  roll,
and the knee pitch. This task is used for the sole purpose of
testing performance when multiple tasks conﬂict. In particular,
the partial joint posture conﬂicts with the CAM task within
the above task set and viceversa. For our test, we use two
hierarchies:
      H1 = {¨x1 →¨x2 →¨x3 →¨x4 →¨x5 →¨x6}
                                                         (32)
      H2 = {¨x1 →¨x3 →¨x4 →¨x5 →¨x2 →¨x6}
The second hierarchy, H2, is more appropriate than the ﬁrst
one, H1  to achieve accurate control of the body shaking
(orientation) task. This is accomplished by assigning higher
priority to the body orientation task and moving backwards the
CAM task. As shown in Fig. 10 (a), changing the hierarchy
levels cause different whole body motions. Fig. 10 (b) shows
the body orientation task error for the two task hierarchies.
The body orientation performance from H2 is better than that
of H1. This can be seen in the interval from 4.0 s to 4.5 s
in Fig. 10 (b). In addition, the different hierarchies cause not
only different movements but also different torque proﬁles. As
shown in Fig. 10 (c), higher torques are needed for H2 than
for H1.


B. Dynamic Walking with Directional Change

  Walking can be broken down into three phases: double
contact, right foot contact, and left foot contact. To represent
these phases we deﬁne the following task hierarchy in WBLC:
    ·  ¨x1 ∈R3: Linear CoM position
    ·  ¨x2 ∈R3: Pelvis Orientation                                         Fig. 11. Continuous walking directional change Valkyrie shows a complex
    ·  ¨x3 ∈R3: Body Orientation                                  dynamic walking pattern involving changing walking direction. (a) shows a
    ·  ¨x4 ∈R3: (for the single contact phases) Foot Orientation    topmappedview tooftheValkyrienext localand itsframe.walkingLocalpath.frames(b) Shosrotatehowwiththetherobot’sdesiredCoMwalkingstate
    ·  ¨x5 ∈R3: (for the single contact phases) Foot Position       direction. For each step, the stance foot becomes the origin of the local frame,
    ·  ¨x6 ∈R6: Neck and Torso Joint Posture                     and the orientation of the frame is aligned with the desired walking direction.
    ·  ¨x7 ∈R3: Centroidal Angular Momentum                  Thethe plannerpreviousﬁndsswitchingthe footCoMplacementstate is projectedwith the newto thestate.current local frame, and
    ·  ¨x8 ∈R10: Arms Joint Posture
To produce swing foot trajectories, we deﬁne third degree B-
splines, which guarantee acceleration continuity. The orien-   C. Push Recovery while Walking
tation coordinates for the robot’s body, pelvis, and feet are
                                                     To validate push recovery, we conduct simulated experi-described using quaternions. For each step, these orientation
                                                       ments under large external disturbances and in various di-tasks are commanded to smoothly switch from the current
                                                                      rections. Although WBLC  is robust to small deviations offrame to next one. Given  initial CoM states, our locomo-
                                                                 the CoM trajectory, for external disturbances we rely on thetion planner computes foot positions and their timing while
                                                               learned recovery policies described in the theory sections.satisfying the desired walking directional changes. In our
                                            When the norm of the CoM state error,test shown in Fig. 11, Valkyrie takes ﬁrst 12 steps while
continuously changing its walking direction by 18.8 ◦per step.                                                                             xd −x
After that, Valkyrie takes 5 forward steps with no directional                 error =                       ,              (33)                                                                                            0.5(˙xd −˙x)
change. Then, Valkyrie takes another 12 steps while changing
direction by, −18.8◦per step. The user only speciﬁes the    is over a threshold equal to 0.05 m and for longer than 0.02s,
walking directions while RL-PSP automatically ﬁnds the foot   our planner computes a new trajectory starting from the current
positions and their timing using the learned policy. The learned  CoM state. Instead of setting the new CoM control goal to be
policy consists only on switching states and step locations.   the current (disturbed) CoM state, we have experienced that it
The desired position, velocity, and acceleration of the CoM    is better to deﬁne a controller goal, xnew, equal to
are computed with the analytic equation of the LIP model at
runtime.                                                           xnew = γxd + (1 −γ)x,              (34)

<!-- PDF page 10 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      10


                                               PSP in the RL formulation, we can quickly ﬁnd locomotion
                                                                    policies for 3D walking. The newly developed WBLC takes
                                                                    into account realistic contact and friction cone constraints.
                                                     At the same time, WBLC maintains task  priorities using
                                                                 projection operators which is missing in previous QP based
                                             WBCs. Overall, WBLC simultaneously exploits the beneﬁts
                                                               of QP based WBC’s and projection based WBC’s, achieving
                                                                         versatility and computational efﬁciency. Another beneﬁt of our
                                                       methods is the planning speed. Our locomotion planner almost
                                                                instantaneously ﬁnds a multistep walking trajectory faster than
                                                                 the state of the art. By devising the replanning process during
                                                      dynamic walking, robots can quickly react to external forces
                                                       and achieve signiﬁcant robustness.
                                                 One interesting aspect of our planning algorithm is the value
                                                               function we used in the learning process. In the future we
                                                           could use this value function as an indicator for walking risk
                                                            given the disturbed states. Many researchers have suggested
                                                                   indicators for locomotion quality. For example, ZMP [22] and
                                           CP [23] are indicators of balance stability but they don’t take
                                                                    into account other important information such as kinematic
                                                                   constraints or swing time limits. Recently, an allowable CoM
                                                                  acceleration region [24] has been proposed for multi-contact
                                                                             stability. However, there  is no indication of kinematic or
                                                      dynamic limitations such as step size or swing time. In contrast
                                                           our value function takes into account some kinematic and
                                                      dynamic constraints that could ultimately make it a versatile
                                                              metric for walking quality evaluation.Fig. 12.  Robustness study. (a) Shows a walking behavior without external
disturbance. (b) When an external impulse of 520 N and 0.1 s duration is     In the future, we will experiment with more complex func-
exerted on the robot’s pelvis, Valkyrie replans its walking trajectories using   tions to represent learned values and policies (e.g. deep neural
the learned policy and maintains its balance without stopping.
                                                              network). In this paper, we have focused on ﬁnding simple
                                                          walking patterns. However, complex neural networks, which
where γ can be selected heuristically, and we use a value of   can represent highly nonlinear and abstract behaviors, can
0.8. In our tests, we push Valkyrie while she is dynamically   enable more versatile planners. For instance, future planners
walking using various disturbance forces applied for a duration  may be able to traverse rough terrain by exploiting various
of 0.1 s. The maximum disturbance impulse that we apply   locomotion modes such as walking, running, or jumping. We
to Valkyrie  is 520 N for 0.1  s. The results are shown in   also plan to implement the proposed algorithms in real systems
Fig. 12 compared to the undisturbed trajectories. The CoM  and evaluate their performance. In our previous work [25],
phase trajectory in the lateral plane shown in Fig. 12 (b) shows  we showed agile bipedal balance with a point-foot biped with
that the planner is able to ﬁnd a new trajectory after an external   series elastic actuators. Since the system is highly unstable
impulse is applied. The time to compute 15 steps after the  by nature, we did not apply external disturbances. We believe
disturbance is less than 1ms using a dual-core 3.0 GHz Intel i7   that the robustness capabilities we have outlined in this paper
processor. At the moment that the replanning process occurs,  may allow us ot accomplish sophisticated behaviors in the real
we also ﬁnd a new swing foot trajectory that transitions from   testbeds.
the original swing trajectory to the new goal.
   Fig. 13 shows results of push recoveries while dynamically
walking when being subject to various external forces. In
all cases, Valkyrie succeeds to sustain the disturbances and                    APPENDIX A
continue walking without stopping. The robustness capabilities    ANALYTIC SOLUTION OF THE PHASE SPACE PLANNER
in this test are competitive to the results of [21] which is not
based on statistical learning. In contrast to this state of the art,    When we constraint PIPM dynamics to a piecewise linear
due to our use of ofﬂine learning our planner is able to come   height surface, z = a(x −px) + b, we can ﬁnd tswitch and py
up with numerous steps almost instantaneously with respect   without numerical integration and bisection search because the
to the walking time frame.                                 system of equations becomes linear, resulting in the following
                                       CoM behavior:
          VI. CONCLUSION AND DISCUSSION
  In this paper, we propose an RL based robust locomo-                   x(t) = Aeωt + Be−ωt + px,
                                                                                                                        (35)
tion planner and a new WBC, dubbed WBLC. By utilizing                       ˙x(t) = ω(Aeωt −Be−ωt),

<!-- PDF page 11 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      11





Fig. 13.  Details of push recovery given various external forces. In this test we demonstrate the ability of Valkyrie to recover from pushes of various
magnitudes and directions. In (a), Valkyrie’s feet collide with each other, but the planner ﬁnds another path that allows it to recover.


where,                                              To ﬁnd the dynamics,  ˙x = f(x), which will lead to the
                                                             switching state solution, let us remove the t term by plugging
         r   g                                Eq. (38) into Eq. (35).
           ω =                    apx + b,
                                            + ω˙x −px       2A                  1                                1                                                     x = Ax                                                 + B                                                          + px      (39)         A =                       (x0 −px) +                                                   ˙x0  ,            (36)                                                        2A                                                                       x + ω˙x −px                  2                         ω

                  1
         B =                       (x0 −px) −1 ˙x0  .
                  2          ω                                                                   1                                                      −px −˙x ) =   2AB˙x               (40)Note  that  this equation  is  the same  for  the y  direction.                2(x      ω   x + ω −px
Based on Eq. (35), we can ﬁnd an analytical solution for                                             ˙x  2
                                                                  (x −px)2 −    = 4AB                 (41)
PSP, summarized  in Algorithm  2.   x1, y1,  xapex,2, and                    ω
xswitch are vector quantities corresponding to the variables
(x1, ˙x1), (y1, ˙y1), (xapex,2, ˙xapex,2), and (xswitch, ˙xswitch).  By performong some algebra we get,
Let us focus on obtaining the step switching time. We can
                                                                                              ˙x2 = ω2((x −px)2 −4AB),
                                                                                                                        (42)
 Algorithm 2: Computation of tswitch, py                                                                                              ˙x2 = ω2 (x −px)2 −(x0 −px)2 + ˙x20,
  Input:  x1, y1, px, ˙xapex, ˙yapex
  Result:  (tswitch, py)
                                                      which yields,
  xswitch ←Find_Switching_State(x1, px, ˙xapex) ;
                           // Eq.(43), (44)        r g
                                                                                                         ˙x = ±                                                                         (x −px)2 −(x0 −px)2 + ˙x20.     (43)   tswitch ←Get_Time(x1, xswtich) ;     // Eq.(38)                                                           h
  tapex ←Get_Time(xswitch, px, xapex) ; // Eq.(38)
                                                       Given two phase trajectories associate with consecutive walk-
  yswitch ←GetState(y1, tswitch) ;     // Eq.(35)
                                                              ing steps, px,1 and px,2 and assuming the robot walks forward,
  py ←Find_Py(yswitch, ˙yapex, tapex) ;  // Eq.(45)                                                                                      i.e. ˙xswitch is positive, we calculate the phase space intersec-
                                                                    tion point via continuity of velocities from Eq. (43):

easily manipulate Eq. (35) to analytical solve for the time
                                                                1    C
variable,                                                             xswitch =        + (px,1 + px,2)
                                                                2  px,2 −px,1
                   1                                                                                                              ˙x20,2 −˙x20,1
              x +    ˙x = 2Aeωt + px,                 C = (x0,1 −px,1)2 −(x0,2 −px,2)2 +
                ω                                                                      ω2
                                                         (37)                                                           (44)
                   1
              x +    ˙x −px = 2Aeωt,
                ω                                        We can now ﬁnd the step switching time by plugging the com-
                                                           puted switching position into Eqs (43) and (38). In addition,which renders
                                             we can obtain the timing at the apex velocity from Eq. (38).
                                  1                        The ﬁnal step is to ﬁnd the y directional foot placement. We                  1    x + ω ˙x −px
                    t =   ln                         .             (38)   ﬁrst calculate yswitch by pluggin tswitch into the y directional
              ω       2A

<!-- PDF page 12 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      12


state equation, which has identical form to Eq. (35). Then, by   Then, we can manipulate the equation above deﬁning ¨q0 to
using the equality that ˙y(tapex) = ˙yapex, we can ﬁnd py,       yield

                  ˙yapex −C                                                                                  ¨q0 = J+2|1  ¨x2 −˙J2J+1 ˙x1 −J2 ˙J+1 ˙x1 −J2J+1 ¨x1                                       ,         py =
          D
                                     −J+2|1 ˙J2|1 ˙q0
          ω               ˙yswitch                                                                                   (55)                                  )eωtapex−      C =                   (yswitch +                                     = J+2|1 n¨x2 −˙J2 ˙q −J2J+1   ¨x1 −˙J1 ˙q o             2                      ω                                                         (45)
                      (yswitch −˙yswitch                                        )e−ωtapex          + J+2|1  ˙J2 ˙q0 −J2J+1 ˙J1 ˙q −J2 ˙J+1 ˙x1 −˙J2|1 ˙q0                        ω
          ω
     D =   (e−ωtapex −eωtapex)             2                                          For simplicity, we deﬁne X ≜¨x2−˙J2 ˙q−J2J+1   ¨x1 −˙J1 ˙q  .
                                                   Then the equation on ¨q0 can be further expressed asAfter calculating py, we can easily get yapex and ˙yapex by
using Eq. (35).                                                                               ¨q0 = J+2|1X + J+2|1 −J2J+1 ˙J1 ˙q −J2 ˙J+1 ˙x1 −J2 ˙N1 ˙q0
                                                    n                                    = J+2|1X + J+2|1 −J2J+1 ˙J1 J+1 ˙x1 + ˙q0                  APPENDIX B
 EQUIVALENT HIERARCHY-BASED JOINT ACCELERATION     −J2 ˙J+1 ˙x1 + J2  ˙J+1 J1 + J+1 ˙J1  ˙q0 o
  The joint velocity associated with an operational task x1 is                                    = J+2|1X + J+2|1 −J2J+1 ˙J1J+1 ˙x1 −J2 ˙J+1 ˙x1 + J2 ˙J+1 J1 ˙q0
                            ˙q = J+1 ˙x1 + N1 ˙q0.                (46)                                                           (56)
                                                       Because J1 ˙q0 = 0, the previous equation becomes
The deﬁnition of the null-space projection matrix using a
pseudo inverse and  its time derivative yields the following       ¨q0 = J+2|1X + J+2|1 −J2J+1 ˙J1J+1 ˙x1 −J2 ˙J+1 ˙x1
expression:
                                     = J+2|1X + J+2|1 J2J+1 J1 ˙J+1 ˙x1 −J2 ˙J+1 ˙x1                                                                                                                        (57)
    N1 = I −J+1 J1 ⇒˙N1 = −˙J+1 J1 −J+1 ˙J1.      (47)     = J+2|1X + J+2|1J2 J+1 J1 −I  ˙J+1 ˙x1
The resulting  joint acceleration can be obtained by time-     = J+2|1X −J+2|1J2N1 ˙J+1 ˙x1.
derivativating equation (46) as described in [13]
                                                           Let us develop the term below using the above expression,
               ¨q = J+1 ¨x1 + ˙J+1 ˙x1 + ˙N1 ˙q0 + N1¨q0           −˙N1J+1 ˙x1 + N1¨q0 = −˙N1J+1 ˙x1 + ¨q0                                                         (48)
       = J+1 ¨x1 + ˙J+1 J1 ˙q + ˙N1 ˙q0 + N1¨q0                   = J+2|1X −˙N1J+1 ˙x1 −J+2|1J2N1 ˙J+1 ˙x1
using the equality ˙J+1 J1 = −˙N1 −J+1 ˙J1 we get                   = J+2|1X +  I −J+2|1J2N1 N1 ˙J+1 ˙x1
                                                                                                              1 ˙x1       ¨q = J+1 ¨x1 −J+1 ˙J1 ˙q −˙N1 ˙q + ˙N1 ˙q0 + N1¨q0     (49)             = J+2|1X + N2|1N1 ˙J+
                                                                                                                        (58)
This allows us to simplify equation (49) to                                                           Thus, equation (50) becomes
            ¨q = J+1   ¨x1 −˙J1 ˙q −˙N1J+1 ˙x1 + N1¨q0.     (50)          ¨q = J+1   ¨x1 −˙J1 ˙q + J+2|1X + N2|1N1 ˙J+1 ˙x1
                                                                                                                        (59)
If we consider a secondary task x2, the term ˙q0 becomes       = J+1   ¨x1 −˙J1 ˙q + J+2|1X + N2|1N1¨qres
                  ˙q0 = (J2N1)+  ˙x2 −J2J+1 ˙x1            (51)                    APPENDIX C
                                                              RELATED WORK
because it can be shown that N1 (J2N1)+ = (J2N1)+, we
                                                             A. Reinforcement Learning based Locomotion Plannerget,
                                                 One of the main challenges for learning robust dynamic
                         ˙q0 = N1 ˙q0                             locomotion policies is handling the high number of continuous                                                         (52)
                         ¨q0 = N1¨q0 + ˙N1 ˙q0.                        variables describing the motion and force interactions of full
                                                     humanoid robots. To deal with the dimensionality problem,
From Eq. (51), the term ¨q0 becomes                   we review previous work that has greatly inspired us. [26],
                                                                solves a periodic locomotion generation problem via RL on a
     ¨q0 = J+2|1  ¨x2 −˙J2J+1 ˙x1 −J2 ˙J+1 ˙x1 −J2J1¨x1            planar biped robot. We advance upon this work by solving the                                                         (53)
    + ˙J+2|1  ˙x2 −J2J+1 ˙x1                                   learning problem for 3D robots, avoiding reliance on human
                                                          walking trajectories, and generating policies for non-periodic
where J2|1 ≜J2N1 and                                              gaits. Other important works employ learning as an optimiza-
                                                                    tion problem over known locomotion  trajectories. In [27],
                  ˙J+2|1 = −J+2|1 ˙J2|1J+2|1.               (54)   a periodic locomotion problems is solved by optimizations

<!-- PDF page 13 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      13


of a known stable central patter generated (CPG) walking   reaction forces as inequality  constraints based on solving
trajectories using RL. However, no focus is given to dealing   a quadratic programming optimization problem with desired
with large external disturbances. In addition, our focus is on   center of mass trajectories. Treatment of reaction forces as
the generation of trajectories from scratch without prior stable   inequality constraints in the WBC communities dates back to
locomotion patterns.                                            the work by [38]. And it showcases one of the weaknesses of
  In [28], robust walking trajectories to external pushes are   our group’s formulation of WBC. In early versions [39] we
achieved based on capture point trajectory optimization via   treated reaction forces as equality constraints. Such treatment
gradient based learning updates. In this work, the capture point   corresponds to bilateral contact constraints, i.e. assuming that
method is used as an analytic controller to initiate the learning   the ﬂoor contacts are actually rigid anchors. This is obviously
process with information about foot placement, step-timing,   an inaccurate model. One of the main objectives of this paper
and ZMP controls. Although the authors also show learning    is to use a realistic unilateral contact model for WBC while
of push recovery strategies without previous capture point   maintaining one of  its main strengths, efﬁcient prioritized
generated trajectories, our focus is stronger on autonomously   control.
learning the locomotion process without reliance on already     Bipedal and quadrupedal walking capabilities have been
stable walking gaits. As such, we belief our algorithm is able   devised  using WBC.  [40] demonstrated locomotion  of a
to learn from scratch recovery strategies in a more generic   quadrupedal robot by utilizing hierarchical tasks based on
sense, for instance to recover from pushes in any direction   least-square problems. The integration of the versatile capture
while walking. Like ours, autonomous learning of periodic   point (CP) as an operational space of WBC was proposed and
gaits has been explored before in passive dynamic walkers   controlled either as a constraint or a task for bipedal humanoid
[29]. Once more, our focus  is on gait generators that can   robots [41]. The robot’s Center of Gravity (CoG) has been used
produce non-periodic gaits and tolerate large push disturbances   as a task controller for a while, such as in [42]. Walking pattern
in all directions of motion.                                     generators have been incorporated into WBC in multiple in-
  The dynamic locomotion community has previously used   stances such as in [43]. During the DARPA robotics challenge,
online optimization methods instead of RL, such as model pre-   several top participants incorporated WBC’s into their strategy
dictive control (MPC). The main problem of these approaches   for achieving mobile dexterous capabilities. For instance, high-
is the high computational  cost. To mitigate  this problem,   level trajectory optimization and low-level optimization with
researchers have made signiﬁcant efforts to develop efﬁcient   inverse dynamics were integrated into the framework by [10].
computational processes. [30] used the gradient of a cost    As stated before, during the DRC several humanoid robots
function to solve the MPC problem efﬁciently. [21] linearized  were controlled via WBC including QP solvers for dealing
the planning problem by optimizing over one step ahead   with reaction  forces. By introducing QP and task  hierar-
of time. Our approach relying on learned neural networks   chy (HQP), whole-body motion of humanoid robots could
replaces the need for complex online computations, enabling   be controlled with the intrinsic reactive advantages of task
the generation of hundreds of steps in an instant compared   prioritization  [44]. Compared with  projection-based WBC
to the stepping time scales. [31] proposed a controller for a   algorithms, optimization-based WBC, such as HQP, can in-
12 DoF biped system by using dynamic programming and a   corporate multiple inequality constraints [12], which are useful
lookup table that was obtained ofﬂine based on simple models.   for describing contact conditions such as friction cones [45].
The multiple policies achieved from each simple model were   Overall, optimization-based WBC have been a success for
combined to control the target system. In contrast, our work   practical applications [9]–[11]. However, their computational
relies on the generic inverted pendulum locomotion model,   cost remains a challenge, specially  if being considered as
and a versatile full-humanoid body controller, i.e., WBLC.     models for motion planning, such as model predictive control.
                                                               Therefore, efﬁciency of our newly proposed whole-body con-
                                                                                troller, dubbed WBLC, is a key consideration of this paper.
B. Whole-Body Control
                                                   To achieve the speed boost, we rely on a projection-base
 WBC [14] is a family of multi and prioritized task-space   formulation. However, it is difﬁcult to incorporate inequality
trajectory controllers for humanoid robots that rely on ﬂoating-   constraints into analytical projection-based methods; thus, our
base dynamic and computed torque commands  as  inputs   goal is to combine both and also to maintain desired task
to the plant.  It yields asymptotically stable control policies   hierarchy capabilities. The proposed WBLC incorporates an
for multiple tasks with simultaneous control of operational   efﬁcient QP, the dimension of which depends only on the num-
forces when needed.  Priorities address resource allocation   ber of contact points, and a joint acceleration level controller
when two or more  task  trajectories cannot physically be  which only relies on projective operators, thus yielding the
tracked by the robotic system. It naturally integrates equality   speed efﬁciency that we advocate for.
constraints such as biarticular transmission constraints [32].
Other groups have explored richer versions of WBC with
                                                        ACKNOWLEDGMENT
inequality constraints such as joint limit avoidance [15], [33],
[34], collision avoidance [35], and singularity avoidance [36].    The  authors would  like  to thank  the members  of  the
Several groups used evolved and more  practical versions  Human Centered Robotics Laboratory at The University of
of WBC such as controllers used in the DARPA Robotics   Texas at Austin for their great help and support. This work
Challenge of 2013 and 2014. For instance, [9], [37] incorporate  was supported by the Ofﬁce of Naval Research, ONR Grant

<!-- PDF page 14 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      14


[grant #N000141512507] and NASA Johnson Space Center,    [24]  S. Caron, Q. Cuong Pham, and Y. Nakamura, “Leveraging Cone Double
NSF/NASA NRI Grant [grant #NNX12AM03G].                        Description for Multi-contact Stability of Humanoids with Applications
                                                                                           to Statics and Dynamics,” in Robotics: Science and Systems.  Robotics:
                                                                               Science and Systems Foundation, Jul. 2015.
                 REFERENCES                                 [25] D. Kim, Y. Zhao, G. Thomas, B. R. Fernandez, and L. Sentis, “Stabi-
                                                                                             lizing Series-Elastic Point-Foot Bipeds Using Whole-Body Operational
 [1] Y. Zhao and L. Sentis, “A three dimensional foot placement planner for        Space Control,” IEEE Transactions on Robotics, vol. 32, no. 6, pp. 1362–
     locomotion in very rough terrains,” in 12th International Conference on        1379, 2016.
    Humanoid Robots (Humanoids), 2012, pp. 726–733.                      [26]  J. Morimoto and C. Atkeson, “Learning Biped Locomotion,” IEEE
 [2]  P. MacAlpine and P. Stone, “Using dynamic rewards to learn a fully         Robotics & Automation Magazine, vol. 14, no. 2, pp. 41–51, 2007.
     holonomic bipedal walk,” in AAMAS Adaptive Learning Agents (ALA),    [27] N. Sugimoto and J. Morimoto, “Phase-dependent trajectory optimiza-
      Valencia, 2012.                                                                     tion for CPG-based biped walking using path integral reinforcement
 [3] C. Graf, A. H¨artl, T. R¨ofer, and T. Laue, “A robust closed-loop gait          learning,” in 13th International Conference on Humanoid Robots (Hu-
      for the standard platform league humanoid,” in A workshop of the 2009         manoids).  IEEE, 2011, pp. 255–260.
    IEEE-RAS Intl. Conf. On Humanoid Robots (Humanoids 2009), 2009.    [28] M. Missura and S. Behnke, “Online learning of foot placement for bal-
 [4]  in Dynamic Walking, Mariehamn, Finland, June 4-9 2017. [Online].        anced bipedal walking,” in 14th International Conference on Humanoid
      Available: http://ruina.tam.cornell.edu/DynamicWalking2017                  Robots (Humanoids).  IEEE, 2014, pp. 322–328.
 [5] A. Herdt, N.  Perrin, and  P.-B. Wieber, “Walking without thinking    [29] R. Tedrake, T. W. Zhang, and H. S. Seung, “Stochastic policy gradient
     about it,” in International Conference on Intelligent Robots and Systems         reinforcement learning on a simple 3D biped,” in International Con-
     (IROS).  IEEE, 2010, pp. 190–195.                                            ference on Intelligent Robots and Systems (IROS).   IEEE, 2004, pp.
 [6]  P. Kryczka,  P. Kormushev, N. G. Tsagarakis, and D. G. Caldwell,        2849–2854 vol.3.
     “Online regeneration of bipedal walking gait pattern optimizing footstep    [30]  T. Erez, K. Lowrey, Y. Tassa, V. Kumar, S. Kolev, and E. Todorov, “An
     placement and timing,” in 2015 IEEE/RSJ International Conference on          integrated system for real-time model predictive control of humanoid
      Intelligent Robots and Systems (IROS).  IEEE, 2015, pp. 3352–3357.           robots,” in 13th International Conference on Humanoid Robots (Hu-
 [7] M. Khadiv, A. Herzog, S. A. A. Moosavian, and L. Righetti, “Step         manoids).  IEEE, 2013, pp. 292–299.
     timing adjustment: A step toward generating robust gaits,” in 2016 IEEE-    [31] E. C. Whitman and C. G. Atkeson, “Control of a walking biped using
    RAS 16th International Conference on Humanoid Robots (Humanoids).         a combination of simple policies,” in 9th International Conference on
     IEEE, 2016, pp. 35–42.                                            Humanoid Robots (Humanoids).  IEEE, 2009, pp. 520–527.
 [8] L. Sentis, “Synthesis and control of whole-body behaviors in humanoid    [32] L. Sentis, J. Petersen, and R. Philippsen, “Implementation and stability
     systems,” Ph.D. dissertation, Stanford, 2007.                                     analysis of prioritized whole-body compliant controllers on a wheeled
 [9]  T. Koolen,  J. Smith, G. Thomas, S. Bertrand,  J. Carff, N. Mertins,        humanoid robot in uneven terrains,” Autonomous Robots, vol. 35, no. 4,
     D. Stephen, P. Abeles,  J. Englsberger, S. Mccrory et  al., “Summary         pp. 301–319, 2013.
      of team ihmc’s virtual robotics challenge entry,” in 13th International    [33]  F. Flacco, A. De Luca, and O. Khatib, “Motion control of redundant
     Conference on Humanoid Robots (Humanoids).  IEEE, 2013, pp. 307–         robots under joint constraints: Saturation in the null space,” in IEEE
     314.                                                                             International Conference on Robotics and Automation (ICRA).  IEEE,
[10]  S. Feng, E. Whitman, X. Xinjilefu, and C. G. Atkeson, “Optimization-        2012, pp. 285–292.
     based full body control for the darpa robotics challenge,” Journal of    [34]  J. Lee, N. Mansard, and J. Park, “Intermediate desired value approach
      Field Robotics, vol. 32, no. 2, pp. 293–312, 2015.                                for task transition of robots in kinematic control,” IEEE Transactions
[11]  S. Kuindersma, F. Permenter, and R. Tedrake, “An efﬁciently solvable        on Robotics, vol. 28, no. 6, pp. 1260–1277, 2012.
      quadratic program for stabilizing dynamic locomotion,” in International    [35] O. Kanoun,  F. Lamiraux, and P.-B. Wieber, “Kinematic control of
     Conference on Robotics and Automation (ICRA).   IEEE, 2014, pp.         redundant manipulators: Generalizing the task-priority framework to
     2589–2594.                                                                       inequality task,” IEEE Transactions on Robotics, vol. 27, no. 4, pp.
[12] L. Saab, O. E. Ramos, F. Keith, N. Mansard, P. Soueres, and J.-Y.        785–792, 2011.
     Fourquet, “Dynamic whole-body motion generation under rigid contacts    [36]  S. Moe, A. R. Teel, G. Antonelli, and K. Y. Pettersen, “Stability analysis
     and other unilateral constraints,” IEEE Transactions on Robotics, vol. 29,          for set-based control within the singularity-robust multiple task-priority
     no. 2, pp. 346–362, 2013.                                                       inverse kinematics framework,” in 54th Annual Conference on Decision
[13] B. Siciliano and  J.-J. Slotine, “A general framework for managing        and Control (CDC).  IEEE, 2015, pp. 171–178.
     multiple tasks in highly redundant robotic systems,” in 5th International    [37] M. Johnson, B. Shrewsbury, S. Bertrand, T. Wu, D. Duran, M. Floyd,
     Conference on Advanced Robotics (ICAR), ’Robots in Unstructured           P. Abeles, D. Stephen, N. Mertins, A. Lesman et al., “Team ihmc’s
     Environments’.  IEEE, 1991, pp. 1211–1216.                                  lessons learned from the darpa robotics challenge  trials,” Journal of
[14] L. Sentis and O. Khatib, “Synthesis of whole-body behaviors through         Field Robotics, vol. 32, no. 2, pp. 192–208, 2015.
      hierarchical control of behavioral primitives,” International Journal of    [38] B. J. Stephens and C. G. Atkeson, “Dynamic balance force control for
    Humanoid Robotics, vol. 2, no. 04, pp. 505–518, 2005.                       compliant humanoid robots,” in Intelligent Robots and Systems (IROS),
[15] N. Mansard, O. Khatib, and A. Kheddar, “A uniﬁed approach to integrate        2010 IEEE/RSJ International Conference on.  IEEE, 2010, pp. 1248–
      unilateral constraints  in the stack of  tasks,” IEEE Transactions on        1255.
     Robotics, vol. 25, no. 3, pp. 670–685, 2009.                              [39] L. Sentis, J. Park, and O. Khatib, “Compliant control of multicontact
[16]  J.  Englsberger, C.  Ott, and A.  Albu-Schaffer, “Three-Dimensional        and center-of-mass behaviors in humanoid robots,” IEEE Transactions
     Bipedal Walking Control Based on Divergent Component of Motion.”        on robotics, vol. 26, no. 3, pp. 483–501, 2010.
    IEEE Transactions on Robotics, vol. 31, no. 2, pp. 355–368, 2015.        [40] M. Hutter, H. Sommer, C. Gehring, M. Hoepﬂinger, M. Bloesch, and
[17]  S. Kajita, F. Kanehiro, and K. Kaneko, “Biped walking pattern gen-        R. Siegwart, “Quadrupedal locomotion using hierarchical operational
      eration by using preview control of zero-moment point,” International         space control,” The International Journal of Robotics Research, vol. 33,
     Conference on Robotics and Automation (ICRA), vol. 2, pp. 1620–1626         no. 8, pp. 1047–1062, 2014.
      vol.2, 2003.                                                              [41] O. E. Ramos, N. Mansard, and P. Soueres, “Whole-body motion integrat-
[18] R. S. Sutton and A. G. Barto, “Reinforcement learning: An introduction,”         ing the capture point in the operational space inverse dynamics control,”
     2011.                                                                               in 14th International Conference on Humanoid Robots (Humanoids).
[19] E. C˘alin, “Multidimensional function approximation using neural net-        IEEE, 2014, pp. 707–712.
     works.”                                                                  [42] M. Mistry,  J. Nakanishi, and S. Schaal, “Task space control with
[20]  J. Kim, “Lie group formulation of articulated rigid body dynamics.”             prioritization for balance and locomotion,” in International Conference
[21] M. Khadiv, A. Herzog, S. A. A. Moosavian, and L.  Righetti, “A        on Intelligent Robots (IROS).  IEEE, 2007, pp. 331–338.
      robust walking controller based on online step location and duration    [43]  J. Carpentier, S. Tonneau, M. Naveau, O. Stasse, and N. Mansard,
     optimization for bipedal locomotion,” arXiv.org, Apr. 2017.                “A  versatile and  efﬁcient  pattern  generator  for  generalized legged
[22] M. VUKOBRATOVI´C and B. BOROVAC, “ZERO-MOMENT POINT         locomotion,” in International Conference on Robotics and Automation
  — THIRTY FIVE YEARS OF ITS LIFE,” International Journal of        (ICRA).  IEEE, 2016, pp. 3555–3561.
    Humanoid Robotics, vol. 01, no. 01, pp. 157–173, Mar. 2004.             [44] A. Escande, N. Mansard, and P.-B. Wieber, “Hierarchical quadratic
[23]  J. E. Pratt and R. Tedrake, “Velocity-Based Stability Margins for Fast        programming: Fast online humanoid-robot motion  generation,” The
     Bipedal Walking,”  in Fast Motions  in Biomechanics and Robotics.         International Journal of Robotics Research, vol. 33, no. 7, pp. 1006–
      Berlin, Heidelberg: Springer Berlin Heidelberg, 2006, pp. 299–324.            1028, 2014.

<!-- PDF page 15 -->

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015                                                                                      15



[45] Y. Abe, M. Da Silva, and  J. Popovi´c, “Multiobjective control with
      frictional contacts,” in ACM SIGGRAPH/Eurographics symposium on
     Computer animation.  Eurographics Association, 2007, pp. 249–258.