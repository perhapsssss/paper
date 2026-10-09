# Extracted source text


<!-- PDF page 1 -->

           Sim-to-Real Learning for Humanoid Box Loco-Manipulation


                                       Jeremy Dao, Helei Duan, Alan Fern




            Abstract— In this work we propose a learning-based approach
           to box loco-manipulation for a humanoid robot. This  is a
           particularly challenging problem due to the need for whole-
         body coordination in order to  lift boxes of varying weight,
            position, and orientation while maintaining balance. To address
            this challenge, we present a sim-to-real reinforcement learning
          approach for training general box pickup and carrying skills for
           the bipedal robot Digit. Our reward functions are designed to
          produce the desired interactions with the box while also valuing
          balance and gait quality. We combine the learned skills into2023    a full system for box loco-manipulation to achieve the task of
         moving boxes from one table to another with a variety of sizes,
           weights, and initial configurations. In addition to quantitativeOct    simulation results, we demonstrate successful sim-to-real transfer
         on the humanoid robot Digit. To our knowledge this is the first
4          demonstration of a learned controller for such a task on real
          world hardware.


                                        I. INTRODUCTION
                                                                              Fig. 1: We learn box loco-manipulation policies in simulation
          Most reinforcement learning (RL) research for legged   and transfer directly to real hardware. We break the task
           robots focuses on locomotion skills such as walking, running,  down into 5 separate policies: WALK, STAND, PICKUP,[cs.RO]
         and navigating various terrains [1–5]. On the other hand,  WALKWITHBOX, and STANDWITHBOX.
         most RL research for object manipulation has focused on                                                                        This paper addresses this challenge by making the follow-
          non-legged robots with fixed or stable bases (e.g. grounded                                                                       ing contribtions:
          robotic arms) [6–8]. RL has been much less explored for
                                                                             • We construct a reward function for learning a “box
          loco-manipulation with legged robots, which involves both
                                                                      pickup” skill and the associated locomotion skills. By
        movement with and manipulation of objects. In particular, we
                                                                           designing these functions with box interaction in mind,
          are unaware of any work that has demonstrated successful
                                                                             specifying when the hands should move to contact the
           sim-to-real RL for loco-manipulation with a bipedal humanoid
                                                                          box, and when to apply forces to move the box, along
           robot. This is a particularly challenging problem due to the
                                                                       with regulating the motion of the hands, we can learn
         need for full-body coordination to manipulate and move
                                                                       smooth, gentle motions that still achieve the task.
           objects while also maintaining balance.
                                                                             • Compared to previous works on locomotion, we find that
          The main goal of this paper is to design and evaluate a
                                                                                     for box pickup using a “relative” action space, where the
           sim-to-real RL approach for loco-manipulation with a real
                                                                             policy outputs are PD setpoint commands to be added
         humanoid robot. In particular, our target task is to walk up
                                                                                    to the current joint position, is more suited for learningarXiv:2310.03191v1    to a box, stop, pick up the box, carry it to another table, and
                                                                  box pickup. This change in action space results in faster
          then set it down. Using data-driven RL for this purpose has
                                                                               learning and less forceful interaction with the box.
          the potential to facilitate generalizion to boxes of different
                                                                             • We present a full box loco-manipulation system where
            sizes, masses, poses, and locations. Designing a sim-to-real
                                                                     each skill, standing and walking with and without a
       RL solution, however, raises a question. There is ambiguity
                                                                          box, and box pickup, is individually learned. We show
          about what is the “best” or most desirable way to pickup
                                                                             successful sim-to-real on the humanoid robot Digit,
         and move a box. How should the hands move, and how
                                                                  which to our knowledge is the first demonstration of a
          should the overall motion of the body coordinate with the
                                                                             learning controller achieving a loco-manipulation task
         hands to produce smooth, non-agressive motion that is still
                                                                 on real world hardware.
          robust? Furthermore, what kind of dense reward signal can
       we provide to faciliate learning such a motion?                                          II. RELATED WORKS

                                                                      A. Loco-Manipulation for Humanoids              *This work is supported by the NSF Grant No. IIS-1849343, DGE-
           1314109, and DARPA Contract W911NF-16-1-0002.                 Much of prior research on loco-manipulation for humanoids
               All authors are with Collaborative Robotics and Intelligent Systems
               Institute, Oregon State University, Corvallis, Oregon, 97331, USA.         has been largely model-based and focuses on mostly static ma-
               Email: {daoje, duanh, afern}@oregonstate.edu.                        nipulation tasks. Model-based approaches have been explored

<!-- PDF page 2 -->

[9, 10] for lifting up boxes, planning a whole-body motion                                              Standing w\
and compensating for the extra force applied by the box.                                          Box
However, these methods produce very conservative motion       Walking            Box Pickup
to ensure absolute stability at all times, resulting in pickup
                                                                                                      Walking w\motions that take over 20 seconds to be completed. Planning
                                                                                          Box
based approaches [11–13] have been explored for producing                  Standing
long loco-manipulation trajectories, with [11] even showing
hardware results. Work focused on locomotion [14, 15] has    Fig. 2: Allowed transitions between the 5 different policies.
explored how to modify a humanoid’s gait when interacting
                                                              standing while holding a box. For each behavior we learn awith objects. These strategies often augment some baseline
                                                                        distinct control policy, which has behavior specific commandgait controller to account for and modify the motion of the
                                                              paramters. Box loco-manipulation involves only a subset ofmanipulated object.
                                                                the possible transitions between these policies. For example,   Prior work that has used learning for humanoid or bi-
                                            we will never go directly from walking to box pickup, andmanual manipulation tasks have been mostly trajectory based
                                                               instead will always use standing as an inbetween behavior.or rely on demonstrations as targets for imitation learning. For
                                                                  Fig. 2 shows the allowed behavior transitions that we targetexample, Seo et al. (2023) uses teleoperation to obtain expert
                                                                   for the box loco-manipulation task.trajectories to imitate, while Liu et al. (2023) uses motion
                                                              All of our policies follow the same general learningtracked human demonstrations for a similar manipulation
                                                       framework, with changes mainly to the reward functiontracking task. This requirement of prior expert data can
                                                                  to learn different skills. Following prior work on bipedalintroduce another failure point in the learning system, as
                                                         locomotion [23] we use an LSTM neural network with twomotion tracking error or alignment error between the human
                                                         128-dimensional recurrent hidden layers to represent ourand robot data can cause componding issues down the line.
                                                                    policies, with the inputs and outputs adapted for the Digit
B. RL for Loco-Manipulation                            humanoid robot, which has 20 DoFs and 10 unactuated joints.
                                                 The input to each policy is a pair (s, c), where s is the 67-  The use of learning for loco manipulation has been largely
                                                            dimensional robot-state vector and is the same for all policies,centered around mobile base or quadraped robots with an
                                                     and c contains a policy specific command. The policy runsattached manipulator arm. Due to the inherent stability of such
                                                                       at 50Hz and outputs actions corresponding to PD setpointa system a common strategy is to separate out the locomotion
                                                                    targets for each actuated joint. These are passed to a PDand manipulation control in to two separate modules. Ma et al.
                                                                   controller running at 2kHz with fixed gains.(2022) utilizes RL for only locomotion while the manipulator
                                          We train policies in simulation using the MuJoCo physicsarm is controlled by a MPC planner, while Sun et al. (2022)
                                                            engine [24] and use the actor-critic PPO algorithm [25] withlearns separate grasping and navigation policies. We utilize a
                                                          a clipped objective and gradient clipping. To facilitate sim-similar separation of locomotion and manipulation skills, in
                                                                      to-real transfer, we use dynamics randomization [26] duringthat locomotion and box pickup are separate control policies,
                                                                  training on parameters such as body mass, joint damping,but unlike Ma et al. (2022) our learned policies control all the
                                                    body center of mass location, and friction. Ranges for thesejoints, so that coordinated full body motion is always possible.
                                                          randomizations can be found in table Table I. Rather thanFu et al. (2022) and Arcari et al. (2022) both learn a more
                                                          use a state estimator during training and testing, we simplyunified control approach that commands both the legs and
                                                           use the true simulation state and apply random noise on topmanipulator arm from the same controller. Fu et al. (2022)
                                                                of it. We train using 80 cores on a dual Intel Xeon Platinumlearns a policy that executes base velocity and end effector
                                                    8280 server.position commands from a higher level planner, while Arcari
                                                     Each of our reward functions is defined in terms of aet al. (2022) learns from a MPC trajectories.
                                                                     distinct set {(ri, wi)} of paired reward terms and weights.  Perhaps the most relevant prior work to our research is Xie
                                                  The corresponding reward function is then defined by:et al. (2023), which targets the same humanoid box pickup
and locomotion task that we do. We follow a similar strategy                                             R = X wiexp(−ri)
of breaking down the task into different skills with a control                                                                                                                                  i
policy for each. The main differences that we try to improve
                                                               In most cases, each of the reward terms will represent someupon is to remove the reliance on trajectory tracking and
                                                                cost to be avoided, so that the negative exponential will befocus more on hardware execution instead of an animation
                                                             smaller for larger costs. The state variables used below tosetting.
                                                                define the reward functions are defined in Table II.
                    III. SYSTEM OVERVIEW
                                                                   IV. LEARNING LOCO-MANIPULATION SKILLS
  We break down the full box loco-manipulation task into 5
                                                             A. Box Pickup Policydistinct behaviors: 1) WALK, for basic walking, 2) STAND, for
transitioning to a standing position after walking, 3) PICKUP,    We want to train a control policy that is capable of picking
for picking up the box, 4) WALKWITHBOX, for walking while   up boxes. It should be able to handle boxes of varying sizes
holding a box, and 5) STANDWITHBOX for transitioning to   and masses, along with the box starting in a range of positions

<!-- PDF page 3 -->

                 Body Mass          [−0.2, 0.2]

                       Joint Damping         [−0.5, 2.5]

                 Ground Friction        [−0.3, 0.2]

               Center of Mass Position   [−0.05, 0.05]

TABLE I: Dynamics randomization ranges. All ranges are in
percentage values, so a range of [−0.2, 0.2] corresponds to a
range of ±20% of the original value.
                                                        target position of x       Fig. 3: Example hand position trajectory for a box pickup.
       px,t     position of x at time t     p∗x,t             at time t         The hands start from the initial robot pose, move to the side
                                                    contact indicator        of the box (shown in blue), make contact with it, and then
                  contact force                   between x and y
     Fx, y                                                  cx, y                                                    (1 if in contact,        bring  it to the target location. In this example the target              between x and y
                                             0 otherwise)          location is directly above the box.
    Φx          roll angle of x       Θx        pitch angle of x                                                      and be on the ground or up to 1.3m in the air. The starting
     vx          velocity of x          ax        acceleration of x       box yaw orientation may be ±22.5◦. The target location is
                  quaternion
     q∗x         orientation of x       pix/y/z     x/y/z position of i       randomized within the same range, except the z position of
                                                               the target will only be above the starting location. The box
     ut        action at time t         τ             torque
                                                                   length, width, and height may each be between 20 to 45cm,
TABLE  II: Definition of state variables used in reward   and the mass may be between 1 to 10kg.
functions.                                      Reward Function. To train box pickup policies, we take
in front the robot. In addition, we aim to learn pickup behavior    inspiration from previous work on learning locomotion
that has smooth, natural motions and timings (e.g. not too fast    policies [5, 23]. Those works described walking through
or too slow). To define the pickup behavior we break it down    stance and swing phases, in other words specifying how and
into two phases: 1) a contact phase, where the hands aim to   when the feet should contact with the ground. This general
make contact with the box, and 2) the lift phase, where the    principal of perscribing contact can be applied to almost
hands aim to move the box to a target position. The phases   any interaction task, and is the main idea we utilize for our
are dictated by hand selected times, relative to the start of   reward function. In contrast to locomotion, box pickup is
the behavior, which is time t = 0. In particular, the contact   a non-periodic behavior and we use a non-periodic clock
phase ends at time tcontact = 100 and then lift phase ends at    signal with phase reference points tcontact and  tlift to define
tlift = 175.                                                     the reward.
  The command input c to the pickup policy consists of: 1)      In particular, the reward function has the form
box dimensions, mass, and starting pose, 2) the target position
                                          R = Rtraj + Rbox + Rstand + Rregto move the box, and 3) two phase indicators pcontact and plift,
which each go linearly from 0 to 1 from the start to end of   where Rtraj rewards hand motion consistent with a box pickup,
each phase. For ease of hardware testing, we assume that the   Rbox is designed to encourage proper interaction with the
box pose is only explicitly known at the start of the behavior.   box, Rstand aims to ensure the robot is stably standing, and
Once the box is picked up and has moved, we approximate    Rreg aims to regulate forces to ensure smoothness and help
the pose with the average pose of the hands, which avoids                                                                sim-to-real transfer. Below we describe the set of reward
the need for real-time estimation of box pose. Given that the   terms used to define each of these components noting that
hands are in contact with the box, it is reasonable to assume    the weights for each term are provided in Table III.
that the box centroid position is going to be roughly between                                                                                Rtraj rewards being close to the target trajectory over time
the hands.                                                     and having a hand orientation of zero using the following
  The action space of box pickup policy differs from the                                                               terms:
locomotion policies. In particular, the locomotion policies add
the policy’s action output to a static “neutral” offset. Rather,           rhand pos = ∥plefthand,t −p∗lefthand,t∥+ ∥prighthand,t −p∗righthand,t∥
for box pickup we found that adding the action output to                                                                               rhand roll = |Φlefthand| + |Φrighthand|
the current motor positions resulted in faster learning (see
Section V). This is likely due to the much larger variance   To describe the desired hand motions, we construct a hand
in motion profile of the pickup behavior from the neutral    position trajectory by choosing three goal hand positions,
position compared to locomotion behavior.                   along with a timestamp for each, and linearly interpolate
Scenario Distribution. At the beginning of each training   between them as shown in Figure 3. For the contact phase,
episode, we spawn a box in a random location in front of the    the hands should first be out along each side of the box, and
robot. The task is then to move the hands to the box, pick it   then eventually actually touching the box along it’s transverse
up, and move it to a randomized target location above the    faces. Since tcontact is 100 timesteps (2 seconds), we design
table. The starting box location may be randomized within 35    the hands to be 10cm besides the box (goal position 1) at 1.5
to 50cm in front of the robot, ±30cm to the side of the robot,   seconds and then at 2 seconds the hands should be on the

<!-- PDF page 4 -->

side faces of the box (goal position 2). The last goal postion      •  If the robot makes contact with the table holding up the
3 occurs at tlift (3.5 seconds) with the hands on either side of        box.
the target location, spaced evenly with a box’s width distance      •  If the box is on the ground.
between them. We were also able to train policies without      •  If it has been 0.5 seconds after the contact countdown
this hand position trajectory. However, we found that these       and the hands are not in contact with the box.
policies trained significantly slower (see section VII) and had      •  If it has been 0.5 seconds after the pickup countdown
less success on hardware.                                    and the box is still in contact with the table.
   Rbox rewards contact with the box at the correct time (not too
early), lifting  it off the table, and moving the box to the target
location with a flat orientation using the following terms:          Name             Weight   Name             Weight

                                                     Hand Position      0.15     Hand Roll          0.05
          rcontact = ln  0.05 · clefthand,box + 0.05 · crighthand,box
                                                   Box Position       0.15     Box Orientation     0.05
        rbox pos = ∥pbox −p∗box∥
                                                                 Table force         0.05     CoP                 0.1
        rbox orient = |Φbox| + |Θbox|
                                                           Base Orientation    0.05       Foot Orientation     0.1          rtable = Ftable,box
                                                         Motor Velocity     0.05       Foot Velocity       0.05

                                                     Hand Force        0.05     Box Acceleration    0.05
It is important to highlight the weighting for rcontact, weight
wcontact = I[t ≥tcontact]·], where I[·] is the indicator function.     Action Change     0.05      Torque             0.05
This causes the contact reward term to only be active at the                                          TABLE III: Reward weightings for the box pickup reward.
end of the first phase, which helps prevent early contact with
the box.
   Rstand rewards the robot for standing stably while picking   Domain Randomization. In addition to the standard dy-
up the box. This is done by keeping the center of pressure   namics randomization we use for all policies, we also add
(CoP) in the middle of the support polygon (or the average   randomization to the policy’s estimate of the box mass
foot location), the torso orientation upright and the feet   (±0.5kg), dimensions (±5cm), and starting location (±5cm).
orientation facing forward, motor velocity small (try to move
as little as possible), and the feet velocities at zero:
                                                             B. Locomotion Policies
           rCoP = ∥pCoP −pavg foot pos∥
             rbase orient = 1 −⟨qtorso, (1, 0, 0, 0)⟩2                To learn locomotion skills we use the same learning setup
                                                              as described in [5, 23] and we refer readers to those works              rfoot orient = (1 −  qleftfoot, (1, 0, 0, 0) 2)+
                                                                  for more details on the reward function. The only changes
                   D             E2                     (1 −   qrightfoot , (1, 0, 0, 0)   )           made for this work was an additional reward term on the hand
                                                                    positions, to keep them in front of the torso and equidistant
             rmotor vel = ∥vmotor∥
                                                      from each other.
               rfeet vel = ∥vleftfoot∥+ ∥vrightfoot ∥                      The box locomotion policies follow largely the same
   Finally, Rreg encourages smooth motions of both the robot   learning setup as the regular locomotion policies, with a
and box itself. It also rewards gentle hand interaction with   few tweaks to accomodate the box. Similar to the box pickup
the box:                                                           policy, the command input c for the box locomotion policy
                                                              contains the box dimensions, mass, and a height command
                raction = ∥ut −ut−1∥                              as input. This height command specifies at what height the
                rtorque = ∥τ∥                                box should be held at while walking.
              rhand force = ∥F hand,box∥+left      ∥F hand,box∥right                  Scenario Distribution. At the start of each training episode
                                                               the robot  is  initialized  to a random  starting pose (see
             rbox acc = ∥abox∥
                                                            Section IV-D for more details), at a random phase in the
The total reward R also has two sparse penalties. There is   walking cycle, and with a random command. The commanded
a −0.1 penalty if there is a self-collision or if the velocity   x  velocity may be randomized between  [−0.5, 1.0]m/s,
of either hand exceeds 1.0 m/s. The weightings of each   y velocity between [−0.3, 0.3]m/s, turning  rate between
dense reward term used is in Table III. To encourage useful   [−π/8, π/8]rad/s, and box height between [1.0, 1.3]m. At
exploration, we also use the following termination conditions,   a random time during the trajectory the commands with be
which encourages learning critical aspects of the behavior   randomized again.
before more detailed aspects.                        Reward Function. The reward function for learning box
   •  If the height of the robot torso is less than 40cm.        locomotion policies is the same as the regular locomotion
   •  If the pitch angle of the robot torso is greater than 35◦.   policies [5, 23] with the addition of a few terms similar to
   •  If either foot loses contact with the ground.               the box pickup rewards. These terms form the box reward

<!-- PDF page 5 -->

we denote as Rbox:                                     D. Skill Transitions

              rbox height = ∥pbox −[0.4, 0, hcmd]∥                Once we have all 5 necessary box loco-manipulation skills,
                                              we need to connect them together in order to achieve the full              rbox orient = |Φbox| + |Θbox|
                                               left                 right                       task. Through out execution, we will transtion from one skill
              rbox force = ∥F hand,box∥+ ∥F hand,box∥                 to another, and the policies need to be able to handle such
              rhand roll = |Φlefthand| + |Φrighthand|                      a transition. Fig. 2 shows the allowed transitions between
                                                                   different policies. Using this we can create a workflow in
There is also an additional termination condition. The box
                                                      which one policy is used to generate an initial state distribution
locomotion policy will always be initialized with a box already
                                                           with which we can use to train the next skill.
in the hands, and it is not allowed to lose contact with the
                                                 More specifically, we first train a regular walking policy.
box else the training episode will terminate.
                                       We then use this to generate many low-speed states fromDomain Randomization. The regular locomotion policy uses
                                                    which we want to transition to standing from. These form
only the base dynamics randomization described in Section III.
                                                               the initial state distribution for training the standing policy.For the box locomotion policy, similar to the box pickup
                                        We can then use the standing policy to generate intial statespolicies, there is randomization to the policy’s box mass
                                                                   for the box pickup policy and so on.(±0.5kg) and dimension (±5cm) input.
                                                   To ensure smooth transitions between policies, we also
C. Standing Policies                                               linearly interpolate between the two policies’ actions over 10
  We want to train standing policies to transition from    timesteps. This action “warmup” is applied during training
walking to static standing states. Since the standing policy   as well, and so during initial state distribution generation we
only has the goal of standing still, there is no c input to the   save the last applied action along with the robot state.
standing policy and it only receives the robot state s.
  The standing box policy has the same goal and learning                  V. SIMULATION RESULTS
setup as the normal standing policy, with only minor mod-
                                          We first conduct quantitative evaluations for the Digit model
ifications to the reward. Since in this case there is a box
                                                                    in the MuJoCo simulator. Each evaluation averages over 10K
that we would like to control, the command input c for the
                                                           episodes using the same episode generation approach as
standing box policy includes the box dimensions, mass, and
                                                              described for training. For example, for the evaluation of the
a box height command.
                                              PICKUP policy we randomly sample box pose, mass, size,
Scenario Distribution. At the start of each training episode
                                                      and target location.
the robot  is  initialized to a random walking  state (see
                                                          Overall Policy Performance. For each of the 5 learned
Section IV-D for more details). For the box standing policy
                                                                    policies we consider an episode a success if: 1) the robot does
the box height command is also randomized.
                                                              not fall over, and 2) the box remains in the robot’s hands at the
Reward Function. The reward function consists of the
                                                       end of the episode for behaviors that involve the box. Further,
following terms (in addition to Rstand and the usual regulator
                                                                    for behaviors that involve the box, we also measure the error
reward Rreg):
                                                                  for successful episodes, which is the distance between the
             rbase vel = ∥vbase∥                                          final position of the box and the commanded target position of
              rheight = |hbase −0.9|                                 the box. Table IV records the success rate and error for each
                                                             of the policies. Overall we see that the policies all achieve
           rarm = ∥pleftarm −[0.15, 0.3, −0.1]∥+                                                          a high success rate and also produce relatively small errors.
                      ∥prightarm −[0.15, −0.3, −0.1]∥                These results show that the policies are all quite robust to the
              rstance width = |(pyleftfoot −pyrightfoot ) −0.385|             randomization of the scenario distribution and the transition
                                                                     starting states that they will typically be initiated in.
              rstance x = |pxleftfoot −pxrightfoot |                                                         Limits of PickUp Policy. We also conducted additional
Note that here pleft\rightarm    denotes the position of the arms in the   simulation experiments for our most complex full-body
torso’s frame. There is also a sparse reward penalty of −0.1   behavior, PickUp. First, we evaluated its performance outside
is there is a self collision. The training episode terminates if   of the training distribution of box parameters. To do this
the robot has fallen over or if either foot is off the ground  we performed an incrementally increasing search for the
after 100 policy timesteps.                          maximum box mass, size, and starting pose that the policy
  The box standing policy follows the same reward function   can successfully pickup. In each test, only one parameter
with the addition of the box reward Rbox described above.   type is varied at a time with all other box parameters kept at
The termination conditions are the same as well, with an    the mean value of the training distribution. In particualar, we
additional termination if either hand loses contact with the   turned domain randomization off and continually incremented
box.                                                          the particular parameter under test until a pickup failure
Domain Randomization. Like the locomotion policies, the   occured. Section V shows that the learned PickUp policy
regular standing policy use only the base dynamics random-   generalizes quite well outside of the training distribution and
ization while the box standing policy has randomization to    is able to pickup boxes much larger and heavier than those
the box mass (±0.5kg) and dimension (±5cm) input.               it saw during training.

<!-- PDF page 6 -->

               PickUp    Stand   StandBox   Walk   WalkBox

    Success %   96.15%   100%    95.25%    96.1%    100%

    Error (cm)     7.93    N/A       1.64     N/A       2.39

TABLE IV: Success rate and accuaracy for the 5 behavior
policies as evaluated over 10K episodes in the MuJoCo
simulator. Each policy is evaluated in a random start state
resulting from a successful run of  its typical preceeding
behavior (e.g. PickUp starts in a Stand end state).


                        Maximum    Training Range

             Mass (kg)           22.9             [1, 10]
                Size (cm)           64            [20, 45]                Fig. 4: Reward curve comparison between different learning
      X displacement (cm)      56            [35, 50]               setups. “Baseline” is the main learning setup we describe
      Y displacement (cm)      41            [-30, 30]               in Section IV-A, “No Hand Trajectory” is the same setup
       Z displacement (cm)      130           [0,130]              without the hand designed hand trajectory in the reward, and
                                                          “Absolute Action Space” adds the policy output to a fixed                Rotation           45◦      [−22.5, 22.5]◦
                                                                 position offset rather than the current motor positions.

                                                    To get the pose of the box during hardware experimentsTABLE V: Test of the box PickUp policy on box parameters
                                            we utilize Digit’s on board RGBD camera and an ArUcooutside of the training distribution. Each row shows the
                                                         marker placed on the box. The box size and mass policy inputmaximum successful value  for the policy  for  that box
                                                                             is hardcoded beforehand. During hardware execution, skillparameter along with the range used for training.
                                                                      transitions, navigation, and walking commands are handled
  PickUp Ablation. We also perform some ablation studies   by a human operator.
on the learning setup with a focus on the PickUp behavior.     Despite the success, we do observe sim-to-real issues on
To test if a simpler reward setup will still learn, we remove   hardware. In particular, we observe policies leaning towards
the hand trajectory tracking reward component. The target   one direction during hardware execution. We suspect this is
location for each hand p∗is instead just the center of the left   due to imu/oriention estimate differences on hardware. To
and right face of the box in the box target position, and does   counteract this, we offset the orientation input in the same
not change throughout the training episode. We found that    direction as the observed leaning. While this “center-of-mass
we can still learn a successful box pickup policy, however,   trim” only needed turning once, it was policy specific. We
the sample efficiency suffers greatly. As can be seen in Fig. 4,   also found that the selected trim values did not work for the
learning without the hand trajectory, approximately doubles    heaviest boxes (8kg), where we observed the policy leaning
the number of samples needed to reach the same reward as   forward, requiring an increase in the trim. We hypthosize that
learning with the trajectory information.                           this error might be caused by force or contact inconsistencies
  Our PickUp policy uses a different action space than the   between simulation and hardware.
locomotion and standing policies. Rather than adding the
policy output to a fixed “neutral” offset robot pose, the PickUp                      VII. CONCLUSION
policy instead adds the policy output to the current joint motor    We presented a learned system for performing box loco-
positions. To test the effect of this change, we train policies   manipulation on the Digit humanoid robot. We broke box
with both action spaces. The reward curves for each are   loco-manipulation down into 5 different behaviors and learn
presented in Fig. 4. As can be seen, using the fixed offset    separate policies for each. We were able to learn policies that
action space learns significantly slower, about as slow as not   achieve high performance in simulation for boxes of varying
using the hand trajectory. We did not observe this same loss   masses, sizes, and starting locations. We also demonstrated
in sample efficiency for the standing and walking policies,   sucessful sim-to-real transfer of those polcies for full loco-
leading us to believe that when the desired motion deviates   manipulaiton episodes, involving walking to a box, pick it
greatly from the fixed position offset, it is beneficial to use a   up, walk to a target location, and setting it down. To our
“relative” action space instead.                           knowledge this is the first such sim-to-real demonstration
                                                              using fully learned policies. Future work will focus on making
               VI. HARDWARE RESULTS                  our system more autonomous by incorporating planning,
  We show successful sim-to-real transfer for all trained    navigation, and vision systems to remove the reliance on
policies, including transitions between each skill. We are able   a human operator and ArUco markers. There is also room to
to perform box pickups for multiple boxes with different   improve our sim-to-real transfer to hardware. For this we will
masses (from 1kg to 8kg) and sizes. The pickup will also   consider both enhancing the domain randomization using in
work for boxes on the ground and those starting on a table. We   simulation based training, and integrating real-world hardware
refer readers to the attached video for hardware experiments.   data from successful and failed trials into the learning process.

<!-- PDF page 7 -->

                 REFERENCES                                 G. Neumann, Eds., vol. 164.  PMLR, 9 2022, pp. 308–319. [Online].
                                                                                      Available: https://proceedings.mlr.press/v164/sun22a.html
 [1] G. A. Castillo, B. Weng, W. Zhang, and A. Hereid, “Robust feedback    [20] Z. Fu, X. Cheng, and D. Pathak, “Deep whole-body control: Learning
     motion policy design using reinforcement learning on a 3d digit bipedal         a unified policy for manipulation and locomotion,” 2022.
      robot,” in 2021 IEEE/RSJ International Conference on Intelligent    [21] E. Arcari, M. V. Minniti, A. Scampicchio, A. Carron, F. Farshidian,
     Robots and Systems (IROS), 2021, pp. 5136–5143.                     M. Hutter, and M. N. Zeilinger, “Bayesian multi-task learning mpc for
 [2] V. Tsounis, M. Alge, J. Lee, F. Farshidian, and M. Hutter, “Deepgait:          robotic mobile manipulation,” 11 2022.
     Planning and control of quadrupedal gaits using deep reinforcement    [22] Z. Xie,  J. Tseng, S. Starke, M. van de Panne, and C. K. Liu,
      learning,” IEEE Robotics and Automation Letters, vol. 5, pp. 3699–         “Hierarchical planning and control for box loco-manipulation,” 6 2023.
     3706, 4 2020. [Online]. Available: http://arxiv.org/abs/1909.08399https:          [Online]. Available: http://arxiv.org/abs/2306.09532
     //ieeexplore.ieee.org/document/9028188/                                 [23]  J. Dao, K. Green, H. Duan, A. Fern, and J. Hurst, “Sim-to-real learning
 [3] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth,          for bipedal locomotion under unsensed dynamic loads.”  IEEE, 5 2022,
     and K. Sreenath, “Reinforcement learning for robust parameterized          pp. 10 449–10 455.
     locomotion control of bipedal robots.”  IEEE, 5 2021, pp. 2811–2817.    [24] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for
      [Online]. Available: https://ieeexplore.ieee.org/document/9560769/            model-based control,” in 2012 IEEE/RSJ International Conference on
 [4]  J. Lee,  J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter,           Intelligent Robots and Systems.  IEEE, 2012, pp. 5026–5033.
     “Learning quadrupedal locomotion over challenging terrain,” Science    [25]  J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov,
     Robotics,  vol.  5,  p.  eabc5986,  10  2020.  [Online].  Available:        “Proximal  Policy  Optimization  Algorithms,”  jul  2017.  [Online].
      http://robotics.sciencemag.org/content/5/47/eabc5986.abstract                   Available: http://arxiv.org/abs/1707.06347
 [5]  J. Siekmann, Y. Godse, A. Fern, and J. Hurst, “Sim-to-real learning of    [26] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-
       all common bipedal gaits via periodic reward composition,” in 2021          to-Real Transfer of Robotic Control with Dynamics Randomization,”
    IEEE International Conference on Robotics and Automation (ICRA),          in 2018 IEEE International Conference on Robotics and Automation
     2021, pp. 7309–7315.                                                   (ICRA).  IEEE, may 2018, pp. 3803–3810. [Online]. Available:
 [6] H. Zhu, A. Gupta, A. Rajeswaran, S. Levine, and V. Kumar, “Dexterous          https://ieeexplore.ieee.org/document/8460528/
     manipulation with deep reinforcement learning: Efficient, general,
     and low-cost,” in 2019 International Conference on Robotics and
     Automation (ICRA), 2019, pp. 3651–3657.
 [7] C. Wang, Q. Zhang, Q. Tian, S. Li, X. Wang, D. Lane, Y. Petillot, and
      S. Wang, “Learning mobile manipulation through deep reinforcement
      learning,” Sensors, vol. 20, p. 939, 2 2020.
 [8] C. Sun, J. Orbik, C. M. Devin, B. H. Yang, A. Gupta, G. Berseth,
     and S. Levine, “Fully autonomous real-world reinforcement learning
     with applications to mobile manipulation,” in Proceedings of the
     5th Conference on Robot Learning,  ser. Proceedings of Machine
     Learning Research, A. Faust, D. Hsu, and G. Neumann, Eds., vol.
     164.  PMLR, 08–11 Nov 2022, pp. 308–319. [Online]. Available:
      https://proceedings.mlr.press/v164/sun22a.html
 [9] H. Arisumi, J.-R. Chardonnet, A. Kheddar, and K. Yokoi, “Dynamic
       lifting motion of humanoid robots.”  IEEE, 4 2007, pp. 2661–2667.
[10] K. Harada, S. Kajita, H. Saito, M. Morisawa, F. Kanehiro, K. Fujiwara,
     K. Kaneko, and H. Hirukawa, “A humanoid robot carrying a heavy
      object.”  IEEE, 2007, pp. 1712–1717.
[11] A. Settimi, D. Caporale, P. Kryczka, M. Ferrati, and L. Pallottino,
     “Motion primitive based random planning for loco-manipulation tasks,”
    IEEE-RAS International Conference on Humanoid Robots, pp. 1059–
     1066, 2016.
[12]  P. Ferrari, M. Cognetti, and G. Oriolo, “Humanoid whole-body planning
      for loco-manipulation tasks,” in Proceedings - IEEE International
     Conference on Robotics and Automation, 2017, pp. 4741–4746.
[13]  S. Karumanchi, K. Edelberg, I. Baldwin, J. Nash, J. Reid, C. Bergh,
       J. Leichty, K. Carpenter, M. Shekels, M. Gildner, D. Newill-Smith,
       J. Carlton, J. Koehler, T. Dobreva, M. Frost, P. Hebert, J. Borders, J. Ma,
     B. Douillard, P. Backes, B. Kennedy, B. Satzinger, C. Lau, K. Byl,
     K. Shankar, and J. Burdick, “Team robosimian: Semi-autonomous
     mobile manipulation at the 2015 darpa robotics challenge finals,”
     Journal of Field Robotics, vol. 34, pp. 305–332, 3 2017.
[14] K. Harada, S. Kajita, F. Kanehiro, K. Fujiwara, K. Kaneko, K. Yokoi,
     and H. Hirukawa, “Real-time planning of humanoid robot’s gait for
      force-controlled manipulation,” IEEE/ASME Transactions on Mecha-
      tronics, vol. 12, pp. 53–62, 2 2007.
[15]  S. Sato, Y. Kojio, K. Kojima, F. Sugai, Y. Kakiuchi, K. Okada, and
    M. Inaba, “Drop prevention control for humanoid robots carrying
     stacked boxes.”  IEEE, 9 2021, pp. 4118–4125.
[16] M. Seo, S. Han, K. Sim, S. H. Bang, C. Gonzalez, L. Sentis, and
     Y. Zhu, “Deep imitation learning for humanoid loco-manipulation
     through human teleoperation,” 2023.
[17]  J. Liu, H. Sim, C. Li, and F. Chen, “Birp: Learning robot generalized
     bimanual coordination using relative parameterization method on human
     demonstration,” 2023.
[18] Y. Ma, F. Farshidian, T. Miki, J. Lee, and M. Hutter, “Combining
     learning-based locomotion policy with model-based manipulation for
     legged mobile manipulators,” IEEE Robotics and Automation Letters,
      vol. 7, pp. 2377–2384, 4 2022.
[19] C. Sun, J. Orbik, C. M. Devin, B. H. Yang, A. Gupta, G. Berseth,
     and S. Levine, “Fully autonomous real-world reinforcement learning
     with applications to mobile manipulation,” A. Faust, D. Hsu, and