<!-- page 1 -->
DROPO: Sim-to-Real Transfer with Ofﬂine Domain Randomization
Gabriele Tibonia,b, Karol Arndtb,∗, Ville Kyrkib
aDept. of Control and Computer Engineering, Politecnico di Torino, Francesco Ferrucci Street, 112, Torino, 10141, Italy
bIntelligent Robotics Group, Dept. of Electrical Engineering and Automation, Aalto University, Maarintie 8, Espoo, 02150, Finland
Abstract
In recent years, domain randomization over dynamics parameters has gained a lot of traction as a method for sim-to-real transfer of
reinforcement learning policies in robotic manipulation; however, ﬁnding optimal randomization distributions can be difﬁcult. In
this paper, we introduce DROPO, a novel method for estimating domain randomization distributions for safe sim-to-real transfer.
Unlike prior work, DROPO only requires a limited, precollected ofﬂine dataset of trajectories, and explicitly models parameter
uncertainty to match real data using a likelihood-based approach. We demonstrate that DROPO is capable of recovering dynamic
parameter distributions in simulation and ﬁnding a distribution capable of compensating for an unmodeled phenomenon. We also
evaluate the method in two zero-shot sim-to-real transfer scenarios, showing successful domain transfer and improved performance
over prior methods.
Keywords: Robot Learning, Transfer Learning, Reinforcement Learning, Domain Randomization
1. Introduction
Over the past decade, there have been signiﬁcant research ad-
vances in reinforcement learning (RL), resulting in a variety of
success stories, from playing Atari games [1] to defeating the
world champion in Go [2]. These successes have sparked a lot
of interest in RL among roboticists; however, due to low sam-
ple efﬁciency of most algorithms, the challenge of accessing
signiﬁcant data collections at training time, as well as the need
for random exploration resulting in the risk of hardware dam-
age, applications of RL in robotics have been lagging behind.
A promising approach to solve the problem of limited data
availability is to use simulated environments for training the
RL agents, and to later deploy them on real-world physical sys-
tems [3–5]. However, while this solves the problem of fast and
safe data collection, inaccuracies in simulation caused by, e.g.,
uncertainty over physical parameters and unmodeled phenom-
ena, may result in policies that do not transfer well to the real
system. Such discrepancy is commonly known as the reality
gap.
One can aim for more generalizable RL agents by perform-
ing the training over multiple variants of the environment, vary-
ing in appearance [5–8], dynamics parameters [4, 9–13], or
both [14, 15]. This technique, known as domain randomiza-
tion (DR), has proven to be successful in a range of robotics se-
tups. However, ﬁnding well-performing domain randomization
distributions over physical parameters can be difﬁcult [16]—the
distributions need to be wide enough to encompass the plausible
true parameter values in the real world, or make up for phenom-
ena which are speciﬁc to the real system but are not modelled
∗Corresponding author.
Email address: karol.arndt@aalto.fi (Karol Arndt)
Human 
demonstrations
Replay in
simulation
Domain 
randomization 
distribution
Policy training
in simulation
Deployment
in the real world
ξ 1
ξ 2
Figure 1: DROPO uses off-policy data or human demonstrations to learn a
domain randomization distribution, which is later used to train a policy that can
be directly transferred to the real world.
in the simulator [17]. At the same time, the DR distribution
needs to allow for convergence while training a single policy
that performs well across all the randomized environments, es-
pecially in the zero-shot transfer scenario. Therefore, there has
been an increasing research interest in developing approaches
to automate DR [18–22].
In this paper, we introduce Domain Randomization Off-
Policy Optimization (DROPO), a novel method for automat-
ically inferring domain randomization distributions. DROPO
ﬁts a dynamics parameter distribution to an ofﬂine dataset us-
ing a likelihood-based metric, which explicitly maximizes the
probability of observing real-world data in simulation. The sim-
Preprint submitted to Robotics and Autonomous Systems
January 13, 2023
arXiv:2201.08434v2  [cs.RO]  12 Jan 2023


<!-- page 2 -->
ulator can thus be thought of as a stochastic forward model
whose randomness arises from variability in the physical pa-
rameters of the scene. Our approach, outlined in Figure 1, de-
parts the trend of online-adaptive DR—where data from the
target domain is collected on-policy during the parameter op-
timization process, requiring iterative access to the real-world
setup [15, 18, 21, 23]—and follows the recently introduced of-
ﬂine setting [20], while using a probabilistic metric to encour-
age variance in the converged parameter distributions. This al-
lows DROPO to optimize DR distributions using only precol-
lected data (e.g. human demonstrations) without suffering from
the distributions collapsing to point estimates due to L2-based
loss functions. In contrast to previous claims [19], our ﬁnd-
ings support that a likelihood-based method can be effortlessly
implemented with a non-differentiable black-box simulator and
gradient-free optimization techniques.
The contributions of this work are: (1) introducing DROPO,
a novel method for ofﬂine optimization of domain randomiza-
tion distributions given safely collected data, (2) an experimen-
tal evaluation of DROPO to show convergence to ground truth
dynamics distributions, (3) demonstrating that domain random-
ization distributions obtained with DROPO can be used to suc-
cessfully train control policies in the presence of unmodeled
phenomena, (4) showing that RL policies can be directly trans-
ferred to the real world when trained in simulation on DROPO’s
dynamics distributions. The source code for running DROPO
with arbitrary ofﬂine datasets is publicly available1.
2. Related work
Domain randomization as a method for training generaliz-
able reinforcement learning policies has been widely studied
over the past few years, both in the context of computer vi-
sion [5–8], dynamics models [4, 9–13] and both at the same
time [14,15]. A major challenge, however, is that domain ran-
domization requires the randomization distributions for each
parameter to be speciﬁed when the model is trained. DR essen-
tially trades optimality for robustness: using too wide ranges
may have negative impact on the training, making it difﬁcult
for the agent to learn a single policy that generalizes to such a
wide range of dynamics, while using too narrow ranges would
bias the model towards a small set of dynamics values and thus
possibly hinder generalization to the real world, as in the case
of system identiﬁcation of point-estimate dynamics [24,25].
To this end, multiple methods for automatically tuning the
randomization ranges were proposed, such as minimizing dis-
crepancy between simulated and real trajectories [21] or di-
rectly maximizing the expected real-world return [23]; how-
ever, as these methods explicitly ask for real-world feedback
during the process, they require access to and careful supervi-
sion of the physical setup in order to run the policy trained on
the intermediate DR distributions.
To relax these requirements, DROID [20] proposed a setting
where the DR distribution is optimized using a ﬁxed, ofﬂine
1https://github.com/gabrieletiboni/dropo
dataset pre-collected in the target domain, aiming to improve
data-efﬁciency and reduce safety risks coming from rolling out
policies trained in unconverged dynamics in contact-rich tasks.
This framework reduced the real-world interaction to a single
data collection step performed before parameter optimization;
additionally, this setting does not make any assumptions about
the data collection procedure, allowing it to be collected with
another policy, or through human demonstrations. Our method
follows the same problem setting, but differs from DROID in
that it uses a likelihood-based objective function and optimizes
the distribution variance in addition to the mean. We provide a
thorough comparison between our method and DROID in Sec-
tion 4.
A variation of this ofﬂine setting, where the real-world data
collection policy is assumed to be available, was addressed in
BayesSim [19]. Under this assumption, BayesSim trains a neu-
ral network to predict dynamics parameter posteriors using tra-
jectories collected in simulation by the given policy under a va-
riety of dynamic conditions. Trajectories collected by the same
policy on the real world setup are then passed to the trained net-
work to predict the dynamics parameter distributions in the real
world. Similar to our work and DROID, BayesSim does not re-
quire access to the real hardware during optimization; however,
it still assumes the data collection policy to be available during
optimization. In contrast, we propose a maximum likelihood-
based framework which does not require the data collection pol-
icy to be known, making it more suitable for use with human
demonstrations. We provide a detailed comparison between our
method and BayesSim with human demonstrations in Section 4.
Other works followed a different approach for applying do-
main randomization, by keeping a ﬁxed range of the physical
parameters and, instead, relying on intelligent sampling tech-
niques to improve generalization: [22] guides training on in-
creasingly harder environment variations, while [26] increases
the number of sampled simulated environments until satisfac-
tory transfer behavior is reached.
Finally, approaches based around differentiable physics sim-
ulators were also devised [27]. While DROPO could in princi-
ple be used with a differentiable simulator, allowing for the use
of a gradient-based optimizer, we do not make any assumptions
about the differentiability of the simulator in this work.
3. Method
3.1. Background and problem formulation
A Markov decision process (MDP) M is described by its
state space S, action space A, initial state distribution p(s0),
state transition distribution p(st+1|st, at) and the reward distribu-
tion p(rt|st, at, st+1). Each episode begins with an agent starting
in state s0 ∼p(s0). At each step, the agent selects an action a
following a policy π(a|s). The problem addressed in reinforce-
ment learning is then to ﬁnd an optimal policy π∗(a|s), such that
the expected cumulative reward (the return) is maximized.
In the domain transfer scenario, we can view the real world
as an MDP with state transition probabilities preal(st+1|st, at),
with the simulation additionally parametrized by the dynam-
ics parameter vector ξ: psim(ssim
t+1|st, at, ξ). We assume that both
2


<!-- page 3 -->
Figure 2: Overview of the main stages of DROPO. The dynamics parameter
distribution is optimized to maximize the probability of observing the collected
dataset in simulation.
MDPs share the state and action spaces, the initial state distri-
bution, and the reward function.
Under this formulation, the problem we address in this work
can be stated as follows: given a dataset of real-world state-
action trajectories D = {s0, a0, s1, . . . , sT}, ﬁnd the distribution
p∗(ξ) such that the likelihood of transitioning to the real state
st+1 when taking action at while in st is maximized over the
dataset:
p∗(ξ) = arg max
p(ξ)
E
st,at,st+1∼D
ξ∼p(ξ)
psim(st+1|st, at, ξ).
(1)
3.2. Method overview
DROPO consists of three main steps: dataset collection on
the real hardware, dynamics distribution ﬁtting, and policy
training. An overview of the method is presented in Figure 2
with a step-by-step walkthrough of dynamics distribution ﬁt-
ting presented in Algorithm 1.
Algorithm 1: DROPO
Result: Parameters φ∗of pφ∗(ξ)
1 Initialize φ to (µinit, Σinit) ;
2 Initialize empty dataset D ;
3 Fill D with trajectories from the target domain ;
4 while not converged do
5
Sample a set Ξ of K random dynamics ξ ∼pφ(ξ) ;
6
forall st, at..t+λ−1, st+λ ∈D do
7
forall ξk ∈Ξ do
8
Set simulator parameters to ξk ;
9
Set the simulator state to st ;
10
Execute actions at..t+λ−1 ;
11
Observe sξk
t+λ ∼psim(ssim
t+λ|st, at..t+λ−1, ξk) ;
12
end
13
Compute the mean ¯sφ
t+λ and covariance Σφ
t+λ (Eq.
2);
14
Evaluate the log-likelihood Lt of st+λ under
N(¯sφ
t+λ, Σφ
t+λ) (Eq. 3);
15
end
16
Compute the total log-likelihood L = P
t Lt;
17
Update φ towards maximizing L ;
18 end
19 Train a policy with DR using the converged pφ∗(ξ) ;
The data collection step is where the dataset D, used for
parameter optimization, is collected on the physical hardware.
This can be done either by running any previously trained pol-
icy (e.g., a policy for another task) or by manually guiding the
robot through kinesthetic teaching. Since DROPO uses ofﬂine,
off-policy data, there is no need to collect additional data at
later stages. This is also the only step where the physical hard-
ware is necessary—all later steps of the method are performed
in simulation, up until the ﬁnal deployment.
The core part of DROPO is the second step, where the do-
main randomization distribution pφ(ξ)—parameterized by φ—
is optimized to maximize the likelihood of real-world data. In
particular, the likelihood is computed w.r.t. the next-state distri-
bution under φ, which can be expressed as the marginal proba-
bility density psim(ssim
t+1|st, at, φ) =
R
psim(ssim
t+1|st, at, ξ)pφ(ξ)dξ.
To approximate this integral, the state-action pair (st, at) in
question is executed multiple times through simulators with dif-
ferent dynamics parameters ξk sampled from pφ(ξ) (steps 7–12
in Algorithm 1). By doing so, the resulting next-state distri-
bution psim(ssim
t+1|st, at, φ) may be estimated, which captures un-
certainty induced by both the simulator dynamics and the given
DR distribution. The parameters φ of pφ(ξ) are then adjusted to
maximize the likelihood of the real st+1 under psim(ssim
t+1|st, at, φ).
We can further generalize the algorithm by allowing to step
the simulator by more than a single step during the inference
process. This mechanism allows to pick a desired evaluation
frequency—regardless of the sampling rate of collected data—
and to increase the signal-to-noise ratio in the difference be-
tween successive states. This results in an additional hyper-
parameter λ ∈N+, which controls how many successive ac-
tions are executed in the environment before evaluating the log-
likelihood of the real st+λ under psim(ssim
t+λ|st, at..t+λ−1, φ). This
generalization is reﬂected in step 10 of Algorithm 1.
Once the parameter optimization process has converged, the
resulting distribution pφ∗(ξ) is used to train a policy in the third
step of DROPO. This policy can then be deployed on the setup
that the data was collected from in the ﬁrst step.
3.3. Data collection
The ﬁrst step of DROPO is to collect the state-action tra-
jectory dataset D, which is going to be used for domain ran-
domization parameter optimization. This dataset can either be
collected from human demonstrations, or by running a previ-
ously trained, safe policy in the environment. Regardless of the
method used, the data should be collected in such a way that al-
lows for identiﬁcation of the relevant dynamics parameters; for
example, it will not be possible for DROPO to infer the friction
coefﬁcient of an object that does not move during demonstra-
tions.
In case demonstrations are provided, the true actions are not
directly known and need to be inferred based on the measured
state sequence using an inverse dynamics model. While learn-
ing inverse dynamics may be a challenging problem in itself, in
certain environments—such as position- or velocity-controlled
robot arms—this inference can be simpliﬁed under the assump-
tions that the robot’s on-board controllers are perfect. While
3


<!-- page 4 -->
this is never the case in real-world systems, we found that
DROPO was able to handle this discrepancy.
Once collected, the dataset is preprocessed in order for the
states to be directly replicable in simulation. First, data from
different sensor modalities needs to be synchronized; this is be-
cause data from position measuring devices, such as motion
capture systems, is likely to be delayed w.r.t. robot joint po-
sition measurements. Additionally, it is necessary to ensure
that the data is sampled with the same frequency as the sim-
ulated environment timesteps. To achieve this, we ﬁt an Akima
spline to all sensor measurements and evaluate it at each envi-
ronment timestep. We chose the Akima interpolation method
over a cubic spline, as it prevents the values from overshooting
in-between sampled points.
3.4. Distribution ﬁtting
Once a preprocessed dataset is available, we move on to the
core part of DROPO—estimating the dynamics probability dis-
tribution pφ(ξ).
In our method, the optimized parameter vector φ includes
both the means and variances of each univariate distribution,
assuming uncorrelated parameters. Therefore, with a dynamics
parameter vector ξ ∈Rd, the parameterization is represented
by a 2d-dimensional vector φ ∈R2d. This is in contrast to
DROID [20], where only the means are optimized while the
standard deviations are taken from the CMA-ES optimization
distribution instead. This change allows to explicitly learn the
variability of each simulated physical parameter to best explain
heteroschedasticity and uncertainty in real-world data. DROPO
can thus be thought as a random coefﬁcient statistical model,
where the optimized coefﬁcients are themselves assumed to be
random variables, as opposed to the more standard ﬁxed-effects
regression analysis.
The distribution ﬁtting process starts with an arbitrary initial
guess φinit = (µinit, Σinit) on the dynamics distribution, roughly
informed by looking at the replayed trajectory in sim.
The
main inference part follows by sampling K dynamics param-
eters from pφ(ξ). Then, for each parameter vector ξk, we set
the simulator state to the original real state st, execute the
real action sequence at..t+λ−1 and observe the next state sξk
t+λ.
This process allows us to estimate the next-state distribution
psim(ssim
t+λ|st, at..t+λ−1, φ), modelled as a Gaussian distribution. In
particular, we infer the corresponding mean and covariance ma-
trix as follows:
¯sφ
t+λ = 1
K
X
k
sξk
t+λ
Σφ
t+λ = d
Cov(psim(ssim
t+λ|st, at..t+λ−1, φ)) + diag(ϵ),
(2)
where d
Cov(·) is the unbiased sample covariance matrix estima-
tor. Here, ϵ is a hyperparameter used to compensate for obser-
vation noise and regularize the likelihood computation in case
singular covariance matrices would appear—e.g. due to direc-
tions of variance in the state-space unexplainable by the sim-
ulator dynamics. Tuning this hyperparameter will, effectively,
adjust how much next-state variance is to be modelled by vari-
ance in dynamics parameters, relative to observation noise. As
demonstrated in our experiments, setting this parameter to too
low values may result in obtaining an overly wide randomiza-
tion distribution: in the extreme case of ϵ = 0, DROPO would
attempt to model all phenomena that cannot be reproduced in
a single simulation by variability in the dynamics, potentially
overﬁtting to noise or unmodeled effects. However, increas-
ing ϵ to excessively large values will eventually lead to over-
regularization and point-estimate dynamics, as all unexplained
variance would be modeled as observation noise, falling back
to pure system identiﬁcation. To ensure stability while promot-
ing variance in the dynamics parameters, we propose to tune ϵ
by increasing it until the Mean Squared Error (MSE) between
real and sim trajectories no longer meaningfully decreases—
similarly to the Elbow method popularly used in machine learn-
ing. We present a thorough analysis of the impact of the ϵ pa-
rameter in the Experiments section.
After observing the resulting simulator states, we make the
assumption that the true, real-world observation st+λ originates
from the next-state distribution induced by dynamics random-
ization: st+λ ∼N(¯sφ
t+λ, Σφ
t+λ)
The log-likelihood of st+λ under this distribution can be then
calculated following the standard Gaussian formula (ignoring
the constant term)
Lt = 1
2(log det Σφ
t+λ + (¯sφ
t+λ −st+λ)⊤Σφ
t+λ
−1(¯sφ
t+λ −st+λ))
(3)
The log-likelihoods of each individual transition can then be
summed to obtain the total log-likelihood of the dataset D under
pφ(ξ): L = P
t Lt
We ﬁnally adjust the parameters φ to maximize the total log-
likelihood L. As we don’t make any assumptions about the dif-
ferentiability of the simulator, we optimize L using a gradient-
free optimization method.
DROPO can, in principle, work
with an arbitrary optimization method; we use CMA-ES [28]
throughout the experiments, with initial scale of 1 and opti-
mization parameters normalized linearly (means) or in log scale
(variances) to the interval [0, 4]. Note that, in order to further
improve stability, we model pφ(ξ) as an uncorrelated truncated
normal distribution bounded to values within two standard devi-
ations away from the mean, with consecutive resampling when
unfeasible parameters are drawn (e.g. negative masses).
3.5. Policy training
The policy π(a|s) is trained for the given target task entirely in
simulation using the converged domain randomization distribu-
tion pφ(ξ). This is achieved by sampling new dynamics param-
eters ξ ∼pφ(ξ) at the start of each training episode. The RL pol-
icy can then be trained with an arbitrary reinforcement learning
algorithm; we use Proximal Policy Optimization (PPO; [29])
and Soft Actor-Critic (SAC; [30]) in our experiments. The tra-
jectories coming from the ofﬂine dataset are not used in any
way during the policy training process; as such, the demonstra-
tions are not required to be speciﬁc to the particular task, as
long as they allow the relevant dynamics parameters to be iden-
tiﬁed.
4


<!-- page 5 -->
4. Experiments
The experimental evaluation aims to answer the following
questions:
1. is DROPO capable of recovering the original dynamics pa-
rameters and randomization distributions in simulated en-
vironments?;
2. is DROPO capable of training a policy that can solve the
task and transfer when unmodeled phenomena are present
in simulation?;
3. how does the value of the ϵ hyperparameter affect the ob-
tained domain randomization distribution?;
4. what is the real-world performance of policies trained with
DROPO compared to DROID [20], BayesSim [19], and
uniform domain randomization (UDR)?
4.1. Benchmark methods
Throughout our experiments we benchmark UDR similarly
to [23], as we assess the average performance of several policies
trained on different uniform bounds. More precisely, we train
10 policies with DR on 10 uniform bounds respectively, which
are randomly sampled from the search spaces reported in the
corresponding tables. This would reﬂect how manually picking
uniform distributions within a reasonable search space affects
the ﬁnal performance.
Furthermore,
in
contrast
to
the
original
paper
on
DROID [20], we replaced torque measurements with the
raw state vectors when implementing the DROID baseline.
This modiﬁcation makes more sense for the pushing and sliding
tasks that we use for evaluation, as joint torques do not express
enough information about the object being manipulated by the
robot, especially for the sliding task—in contrast to the door
opening task used in the original DROID paper. The CMA-ES
implementation used in DROPO and DROID is provided by
Nevergrad [31].
Finally, in order to adapt BayesSim to the ofﬂine setting
with human demonstrations (where the data collection policy
is not available), we repeat the original action sequence dur-
ing data collection. Besides this modiﬁcation, we make use of
the original open-source repository provided by [19]. In most
experiments, we evaluate both neural network (MDNN) and
quasi-random Fourier (MDRFF) features and report the better
result for brevity. An exception to this is the sim-to-real ex-
periment with the Panda robot, where results with both features
are reported in order to compare the generalization capability of
both variants. Since BayesSim uses mixture Gaussian distribu-
tions, the distribution inference results reported in the tables and
plots in this section are independent Gaussian approximations
of the complete results, for the sake of brevity. The complete
BayesSim posteriors can be found in Appendix D.2.
4.2. Hopper
In the Hopper environment [32], a one-legged robot is tasked
to learn to jump forward as fast as possible without falling
down. This environment has been used as a standard control
benchmark in a variety of papers [18, 29, 30, 33]. We intro-
duce parameter randomization to this environment by varying
the mass of each link. We use this environment as a simple
benchmark to test DROPO’s capability of identifying the dy-
namic parameters of the system and recovering the parameter
distribution that was used to generate the dataset. We later in-
troduce an unmodeled effect in the form of a misspeciﬁed mass
(which is not included in the optimization problem), similarly
to [18]. Given the simple sim-to-sim scenario, the ofﬂine tra-
jectories for running DROPO have been collected by rolling out
semi-converged policies trained directly in the target domain.
4.2.1. Point-dynamics system identiﬁcation
When the ofﬂine dataset is collected on a single Hopper en-
vironment instance, DROPO is expected to identify the target
physical parameters and to converge to point-estimate dynamics
rather than distributions. We tested this behavior on the Hopper
environment by collecting two trajectories (1000 state transi-
tions corresponding to 8 seconds of wall time) on the ground
truth dynamics shown in Table 1, both with and without noise
of variance 10−5 injected in the ofﬂine observations. The results
are reported in the same table, as DROPO achieved convergence
to the original dynamics regardless of the presence of noise and
effectively decreased the standard deviation of learned param-
eters to 10−5, set as the lowest bound during the optimization
problem.
In the point-estimate dynamics estimation, DROID also con-
verged to the ground-truth parameter values, with a lower stan-
dard deviation than DROPO (as CMA-ES does not impose any
lower bounds on the variance). Thus, both DROPO and DROID
perform virtually the same in this benchmark.
On the other hand, BayesSim overestimates the distribution
variance and does not accurately recover the mean parameter
value.
This is in line with the results reported in the orig-
inal paper [19], where the resulting posterior distribution is
much wider than the ground-truth values used for data gen-
eration. While wider distributions may beneﬁt generalization,
BayesSim falls short of DROID and DROPO in terms of pure
system identiﬁcation capabilities.
4.2.2. Recovering the dynamics distribution
In this experiment, the dataset D was collected while vary-
ing the target dynamics according to some ground truth dis-
tribution p(ξ), which we want to recover. We collected two
trajectories on the Hopper environment, varying all masses as
mi ∼N(µi, 0.252) around their original values µi every 25
state transitions, except for the torso mass which was kept
ﬁxed. Since BayesSim expects the input to be trajectories col-
lected from a single dynamics setting rather than a set of transi-
tions, we had to use a different test procedure for this baseline;
namely, we sample multiple dynamics conditions from the true
distribution and run BayesSim individually for each of them.
The resulting distribution is then obtained by marginalizing the
output distribution over the input dynamics distribution.
The results are reported in Figure 3, which shows DROPO
successfully learning the original variance of the randomized
5


<!-- page 6 -->
3.2
3.3
3.4
3.5
Torso mass
3.6
3.8
4.0
4.2
4.4
4.6
Thigh mass
DROPO
DROID
BayesSim DROPO
(noisy)
DROID
(noisy)
BayesSim
(noisy)
2.4
2.6
2.8
3.0
Leg mass
DROPO
DROID
BayesSim DROPO
(noisy)
DROID
(noisy)
BayesSim
(noisy)
4.6
4.8
5.0
5.2
5.4
Foot mass
Figure 3: Dynamics distributions optimized by DROPO, DROID and BayesSim
on ofﬂine data collected from a distribution of Hopper environments (blue
shaded areas). The distributions are displayed with 2σ-wide ranges centered
on their means.
masses, in addition to their means. We believe that such ex-
plainability is only possible when explicitly optimizing param-
eters through probabilistic distance metrics, as DROID’s L2-
based cost function fails at providing wide distribution ranges
on the randomized masses. Note how BayesSim, while pre-
serving some variance in the converged distributions, resulted
in much less accurate dynamics distribution estimates. Analo-
gously to the previous experiment, a noisy version of the dataset
has also been tested, yielding similar results.
4.2.3. Unmodeled phenomena
Finally, we also tested DROPO’s ability to compensate for
unmodeled phenomena in simulation by assessing the complete
transfer to a target simulator from an under-modeled source do-
main. We introduced such unmodeled effect by misspecifying
the Hopper torso mass by 1kg in the source simulator and ex-
cluding it from the optimization space. Hence, each method
may only optimize the means and variances of the remaining
three masses to match the target transitions, and cannot adjust
the incorrect torso mass.
To perform this evaluation, we ﬁrst ran each method to infer
the dynamics distribution given the same noiseless data as in
Section 4.2.1. Since there are no ground-truth domain param-
eter values that could be used as a reference when unmodeled
phenomena are present, the domain randomization distributions
cannot directly be used to quantitatively compare the estimated
dynamics parameters. Instead, we used the obtained distribu-
tions for policy training in the environment with a misspeciﬁed
mass, and evaluated the resulting policies in the original envi-
ronment where data was collected. We repeated this process 3
times for each method, with different random seeds. The poli-
cies were trained with SAC [30].
The results of this evaluation are presented in Figure 4, to-
gether with a policy trained directly in the target environment
to provide a notion of the upper bound. We observe that policies
trained with DROPO’s randomization distributions outperform
all baseline methods, almost matching the policy trained in the
ground-truth environment in terms of performance. At the same
time, the policies obtained with DROID and BayesSim perform
much worse. Note how some UDR policies are at times able
to generalize well to the target environment, suggesting that the
task could be solved by manual trial and error with different
True env DROPO
DROID
UDR
BayesSim
500
1000
1500
2000
Return
Figure 4: Sim-to-sim: episode returns in the target Hopper environment, com-
paring policies trained directly in the target environment, and trained in the
environment with a misspeciﬁed torso mass using domain randomization dis-
tributions inferred by DROID, DROPO and BayesSim.
uniform bounds.
To provide more insight into these results, we can look at the
converged domain randomization distribution reported in Ta-
ble 1. Note how, even though the target dataset has been col-
lected on point-dynamics parameters, DROPO converges to a
distribution over the three randomized masses. This behavior is
indeed expected, as due to the unmodeled phenomenon intro-
duced, a single point-estimate parameter vector is not able to
accurately reproduce all transitions in the target dataset. There-
fore, DROPO widens the dynamics distribution to maximize
the likelihood of target-domain data to be observed in simula-
tion. In addition, the optimized means are now much different
from the ground truth parameters. On the other hand, the results
show that—just like in the distribution recovery experiments—
DROID is eager to converge to point-estimate parameters, in
order to minimize the L2-distance based objective function (see
Appendix A for an intuitive explanation of this phenomenon).
Such a policy performs well in the training environment, but
fails to generalize to the test conditions.
Furthermore, notice how BayesSim produced distributions
with means located close the center of the search space with
large standard deviations. As such, it was able to learn a suc-
cessful policy that works over a range of dynamics parameters,
including the environment where the unmodeled phenomenon
is present. However, excessively large standard deviations re-
sult in overly conservative policies that produce a slower for-
ward motion than DROPO, resulting in a lower return.
We
suspect that this might be caused by the domain shift between
the training data collected from the simulation with misspeci-
ﬁed mass and the data from the real environment used to in-
fer the randomization distribution. In BayesSim, the inference
network is trained on trajectories obtained from the simulator,
each collected in different dynamics conditions. As a result, any
trajectory that cannot be reproduced by single dynamics condi-
tions in simulation will effectively lie outside of the inference
network’s training domain. Thus, we claim that any task involv-
ing unmodeled phenomena or unmodeled noise is substantially
difﬁcult for the BayesSim neural network, as the evaluation do-
main does not match the training domain anymore. Later, we
obtained similar results in the Panda sim-to-real experiments,
as described in Section 4.3.2.
To summarize, we observe that a combination of both system
6


<!-- page 7 -->
Masses (kg)
m1
m2
m3
m4
Ground truth
3.534
3.927
2.714
5.089
min
1.767
1.963
1.357
2.545
Search
space
max
7.069
7.854
5.429
10.18
µ∗
3.534
3.927
2.714
5.089
DROPO
ϵ=1e−8
σ∗
1.0e-5
1.1e-5
1.1e-5
1.0e-5
µ∗
3.534
3.927
2.714
5.089
DROID
σ∗
1.2e-12
2.1e-12
2.0e-12
1.1e-12
Noiseless
µ∗
3.350
5.342
3.994
5.560
BayesSim
σ∗
0.697
0.707
0.686
0.541
µ∗
3.531
3.931
2.717
5.093
DROPO
ϵ=1e−5
σ∗
8.1e-3
1.3e-3
1.3e-3
2.4e-4
µ∗
3.534
3.927
2.714
5.089
DROID
σ∗
1.2e-12
2.4e-11
2.0e-12
1.2e-12
µ∗
6.295
4.002
3.486
3.771
Noisy
BayesSim
σ∗
0.218
0.257
0.245
0.256
µ∗
4.707
3.181
4.385
DROPO
ϵ=1e−3
σ∗
2.534
(ﬁxed)
0.667
0.206
0.826
µ∗
4.021
3.591
4.845
DROID
σ∗
2.534
(ﬁxed)
6.0e-6
1.7e-6
4.2e-6
µ∗
3.493
2.901
4.596
Unmodeled
BayesSim
σ∗
2.534
(ﬁxed)
1.576
1.471
1.537
Table 1: Optimized dynamics distributions on Hopper OpenAI Gym environ-
ment. The ground truth values indicate the simulator instance used during data
collection.
identiﬁcation and domain randomization is essential to solve
the task under this unmodeled effect, as neither UDR—pure un-
optimized domain randomization—nor DROID—which con-
verged to a point-estimate—result in a successful zero-shot
transfer.
4.2.4. The domain variance–observation noise tradeoff
Throughout our experiments, we observed that introducing
the ϵ hyperparameter is generally beneﬁcial to obtain more sta-
ble and sound results (see Section 3). This turned out to be
particularly effective when optimizing the estimated likelihood
function in presence of noise or unmodeled effects. However,
overly large values of ϵ should be avoided to prevent DROPO
from converging to point-estimate dynamics parameters. To
study this trade-off, we report a thorough sensitivity analysis
on this hyperparameter, showing its impact on the ﬁnal perfor-
mance of DROPO for the previously described Hopper experi-
ments and describing our tuning procedure in more detail.
The results of point-dynamics recovery in Hopper with vary-
ing ϵ are presented in Figure 5. We observe that, for a low
value of ϵ, DROPO overestimates the standard deviation in
the noisy setting, as it attempts to explain the random varia-
tion in next-states by variance in dynamics. However, for ϵ
values equal to the noise variance (or higher), DROPO con-
verges to very low standard deviations, corresponding to a
point-estimate of dynamics parameters and leading to a signif-
icant drop in MSE. The MSE is computed w.r.t. the converged
distribution φ∗obtained by DROPO, as follows: MS E(φ∗) =
P
t ∥(¯sφ∗
t+1 −st+1)∥2. This metric resembles the trajectory dis-
crepancy function adopted by previous works [20, 21], and we
propose to use it as a reference to reach a stable optimization
process and account for observation noise when tuning ϵ. Note
how, in the same ﬁgure, the MSE drop is not as clear for the
noiseless setting: here, ϵ only serves the purpose to regularize
the log-likelihood computation, which could be ill-conditioned
with too low values (e.g. ϵ = 10−10 in Figure 5b) as close-to-
singular covariance matrices may appear when estimating the
10
9
10
7
10
5
10
3
10
1
Epsilon
0
1
2
3
4
5
6
Value
Torsomass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
1
2
3
4
5
6
7
Value
Thighmass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
0
1
2
3
4
5
6
Value
Legmass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
2.5
3.0
3.5
4.0
4.5
5.0
5.5
6.0
Value
Footmass
Noiseless
Noisy
Ground truth
Hopper distributions (mean and standard deviation)
(a)
10
9
10
7
10
5
10
3
10
1
epsilon
10
14
10
12
10
10
10
8
10
6
10
4
10
2
mse
Hopper MSE
Noisy
Noiseless
(b)
Figure 5: Epsilon sweep on point-estimate dynamics recovery: (a) shows the
converged distributions in the noiseless and noisy (σ2 = 10−5) cases, (b) shows
how the MSE changes with ϵ. (results averaged over 4 random seeds)
10
9
10
7
10
5
10
3
10
1
Epsilon
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
Value
Torsomass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
2
3
4
5
6
Value
Thighmass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
1.5
2.0
2.5
3.0
3.5
4.0
4.5
5.0
Value
Legmass
Noiseless
Noisy
Ground truth
10
9
10
7
10
5
10
3
10
1
Epsilon
3
4
5
6
7
Value
Footmass
Noiseless
Noisy
Ground truth
Hopper distributions (mean and standard deviation)
(a)
10
9
10
7
10
5
10
3
10
1
epsilon
10
4
10
3
10
2
10
1
mse
Hopper MSE
Noisy
Noiseless
(b)
Figure 6: Epsilon sweep on dynamics distribution recovery: (a) shows the con-
verged distributions in the noiseless and noisy (σ2 = 10−5) cases, (b) shows
how the MSE changes with ϵ. (results averaged over 4 random seeds)
next-state distribution2.
We observe a similar phenomenon in the dynamics distribu-
tion recovery scenario (Figure 6). Small ϵ values result in an
excessively large variance in masses in presence of noise, while
correctly identifying the ground-truth distribution in the noise-
less case. As ϵ grows larger, more of the variety in next-states
gets attributed to noise and the estimated dynamics distributions
move towards point dynamics, both in the noisy and noiseless
case. The best ground-truth distribution recovery is observed
when ϵ matches the true noise variance, which also corresponds
to the sharp drop in MSE observed in Figure 6b—thus validat-
ing the proposed tuning process.
Finally, we report similar observations for the unmodeled
phenomenon experiment (Figure 7), where—as ϵ increases—
unexplainable effects in state space due to under-modeled dy-
namics get attributed to noise, stabilizing the optimization prob-
lem. Once again, we tuned ϵ based on the MSE observed in
Figure 7b, and picked ϵ = 10−3, which is where the MSE val-
ues stop to meaningfully improve. As observed in Figure 7a,
this value closely approximates the mean obtained with higher
ϵ values, while preventing the distribution from collapsing due
to excessive regularization. To this end, we would like to em-
phasize that a conservative choice may always be made with
DROPO when tuning the value of ϵ: higher values will only
shift DROPO towards lower standard deviations (eventually
2Adding a small value ϵ to the diagonal of an ill-conditioned covariance
matrix has the effect to increase all eigenvalues by ϵ, thus making the likelihood
computation more stable.
7


<!-- page 8 -->
10−9
10−7
10−5
10−3
10−1
Epsilon
1
2
3
4
5
Value
Thighmass
10−9
10−7
10−5
10−3
10−1
Epsilon
0
1
2
3
4
5
6
Value
Legmass
10−9
10−7
10−5
10−3
10−1
Epsilon
0
1
2
3
4
5
6
Value
Footmass
Hopper distributions (mean and standard deviation)
(a)
10−9
10−7
10−5
10−3
10−1
Epsilon
0.002
0.004
0.006
0.008
mse
Hopper MSE
(b)
Figure 7: Epsilon sweep on the unmodeled phenomenon experiment: (a) shows
the converged distributions, (b) shows how the MSE changes with ϵ. (means
and variances averaged over 8 seeds)
GT
DROPO DROID
UDR BayesSim
0
500
1000
1500
2000
2500
3000
Return
Figure 8: Sim-to-sim: episode returns in the target simulated environment when
trained on domain randomization distributions inferred by DROID, DROPO
and BayesSim and on the ground-truth dynamics distribution (GT) in the Panda
pushing task.
providing similar results to DROID), while allowing a desirably
low MSE to be obtained.
Note how the proposed tuning procedure draws similarities
to the elbow method popularly used in machine learning, e.g.
to ﬁnd the best number of clusters in clustering analysis or the
number of principle components to retain in principal compo-
nent analysis.
4.3. Robotics experiments
We further evaluate DROPO on two sim-to-real robotics se-
tups: a hockey puck sliding and a box pushing task.
4.3.1. HockeyPuck
In the HockeyPuck setup, the Kuka LWR4+ is equipped with
a hockey stick and tasked with hitting a hockey puck such that
(a)
(b)
Figure 9: The hockeypuck setup in simulation (a) and in the real-world (b). The
purple area in (a) shows the range of possible goal positions.
DROPO
DROID
UDR
0
10
20
30
40
Distance (cm)
Figure 10: Sim-to-real performance in terms of the ﬁnal distance to the target
position on the hockeypuck setup (in centimeters; lower is better).
it stops at the given target location. For this setup, we use an ice
hockey puck and a whiteboard as a low-friction surface for the
puck to slide on. The simulation environment is built in Mu-
JoCo [34] akin to the real-world setup. Both setups are shown
in Figure 9. The yellow puck and the purple area in Figure 9a
show the initial position of the puck and the range of possible
goal positions.
In this setup, the actions are whole hitting trajectories; this
is achieved by ﬁrst training a variational autoencoder (VAE) on
a range of task-speciﬁc trajectories, and later using the decoder
as a trajectory generator, with actions given in the latent space
of the VAE, following [6,35]. This simpliﬁes the reinforcement
learning problem by turning it into a contextual multi-armed
bandit problem.
The demonstrations for optimizing the parameter distribution
are obtained by rolling out 5 random trajectories of 750 transi-
tions (or 7.5 seconds) each, sampled from the latent space of the
VAE (z ∼N(0, I)). The joint positions are obtained using the
robot’s internal sensors, while the positions of the hockey puck
are obtained with OptiTrack, a motion capture system, with the
frequency of 120Hz. During the post-processing, the data is
synchronized, the positions are resampled to match the simu-
lated timesteps of the simulated environment, and the velocities
are obtained by taking the derivative of the spline used to re-
sample the signal.
The state space used for dynamics ﬁtting with DROPO con-
tains the positions and velocities of the robot joints and the
hockey puck. The use of a trajectory generator allows us to
use original commanded velocities as actions when replaying
trajectories in the simulator, and—on this particular setup—
removes the need of action inference from demonstrations.
We randomize a total of 18 dynamics parameters: the mass
of the puck, the puck-surface friction coefﬁcients, the time con-
stant of the stick-puck contact—regulating the stiffness and
damping while keeping the interaction critically damped—and
the gains of the position controller used in simulation. Note
that, while more parameters may be added to the optimization
problem to increase the model’s explanatory power, complex
correlations between the parameters may arise in addition to a
generally higher complexity.
We use the reward function of [36]: r = −d2 −log(d + α),
where d is the distance to the target and α is a constant (we use
α = 10−3 throughout the experiments).
The results comparing DROPO, DROID and UDR are shown
8


<!-- page 9 -->
m
fx
fy
tconst
Search
space
min
0.08
0.2
0.2
0.001
max
0.2
0.75
0.75
0.02
DROPO
ϵ=1e−2
µ∗
0.111
0.349
0.231
0.019
σ∗
2.2e-04
3.4e-05
4.7e-04
6.7e-05
DROID
µ∗
0.100
0.334
0.226
0.019
σ∗
1.5e-07
8.9e-06
9.7e-06
1.7e-05
Table 2: Optimized dynamics distributions on 5 trajectories collected on the
Hockeypuck environment. The converged mass m, friction coefﬁcients fx and
fy along the two axes, and timeconst parameter tconst are reported.
(a)
(b)
(c)
Figure 11: The push setup in simulation (a) and in the real world (b), with the
insides of the box shown in (c).
in Figure 10. We see that, on this setup, both DROPO and
DROID signiﬁcantly outperformed UDR, and that there was no
signiﬁcant difference between the two methods, despite DROID
essentially converging to point estimates (see Table 2). This is
likely caused by the bandit formulation and the resulting feed-
forward nature of the task; once the action is selected, the agent
does not receive any feedback from the environment. Under
this setup, it is thus optimal for the policy to select the action
(or the trajectory) which minimizes the expected ﬁnal distance
from the target position under the dynamics distribution used in
training. This closely resembles the optimization criterion used
by DROID (minimizing the expected L2 norm between trajec-
tories). Additionally, under this formulation the policy lacks the
ability to make up for possible deviations from the trajectory
obtained in point-estimate dynamics. In a sequential decision
making problem with uncertain dynamics, the agent needs to
be able to recover from a wider range of states, due to the un-
certainty in state transitions that stems from the uncertainty in
dynamics. In a bandit problem, however, the system operates in
a feedforward manner, and thus is not able to handle such situ-
ations at all. As a result, the beneﬁts of having a distribution of
dynamics are diminished.
4.3.2. Pushing
We ﬁnally evaluated DROPO on a pushing task with the
Franka Panda robot. In this setup, shown in Figure 11, the goal
of the robot was to push a box to a ﬁxed target position. To
make this task more challenging, the box center of mass was
altered by ﬁlling it up with heavy steel bolts on one side and
bubble wrap on the other, as shown in Figure 11c. Therefore,
we randomize a total of 5 dynamics parameters to shorten the
reality gap in this setup: mass of the box, box-table friction
coefﬁcients fx and fy, and center of mass offset from the geo-
metric center (comx, comy). Due to the offset center of mass,
we additionally included the orientations and angular velocity
of the box in the state space used for ﬁtting DROPO.
In order to model log-likelihood of orientations with
DROPO, we used quaternion representations and evaluated the
angle between the quaternion in the real-world dataset and the
one in simulation; this angle, α, then replaced the orientation in-
side the next state sξ
t+1, with α inside the real-world state vector
set to 0. Since such a distribution would not be well-modeled
with a Gaussian, for each transition we insert two resulting next
states (with α and −α), resulting in a symmetric distribution of
angles centered around 0.
We ﬁrst tested our method in a sim-to-sim version of the task:
synthetic data was collected by a forward-pushing policy as
demonstrations for DROPO, DROID and BayesSim, sampling
new dynamics parameters from the ground-truth distribution af-
ter every rollout, for a total of 50 trajectories of 30 transitions
each, amounting to 30 seconds of wall-time interaction. The
resulting DR distributions are presented in Table 3. Like be-
fore, the reported BayesSim results are independent Gaussian
approximations of the actual results, which can be found in Ap-
pendix D.2. We again observe that DROID converged to a
point estimate, with standard deviations in the order of 10−10–
10−11, while DROPO results in a distribution that is relatively
close to the ground truth, albeit not the same. The largest dis-
crepancy can be observed in the inferred friction value along
the x direction. Since the trajectory used for this demonstra-
tion was pushing the box primarily away from the robot (along
the y axis), accurately inferring friction along the lateral axis
is challenging, and the variations in box motion resulting from
variations in this friction are minor and can be reasonably well
modeled by variation in other parameters. Similarly, the mass
of the box can also be relatively difﬁcult to identify, given that
the inference is performed with a position controller and the
mass of the box is much smaller than the mass of the robot.
We then used these DR distributions to train a policy for
pushing the box to a goal on the front-left side of the robot.
We used the same reward function as for the Hockey experi-
ments, with additional control penalties added to regularize the
motions and to deter the simulated robot from going over the
velocity and acceleration limits of the physical robot arm. The
performance of each policy is shown in Figure 8. We observe
that, despite the converged distribution being slightly different
than the ground truth, the policies trained with DROPO per-
formed close to the ground truth policies, while DROID poli-
cies performed noticeably worse, likely due to overﬁtting to
point-estimate dynamics. Interestingly, the UDR baseline out-
performed DROID too. This suggests that, for the underly-
ing task, DR is a more effective transfer technique than system
identiﬁcation even when the distribution is not carefully tuned;
in other words, wider but less accurate dynamics parameter dis-
tributions provide better results than converged point estimate
parameter values.
We then evaluated DROPO’s ability to transfer to the real-
world setup, in comparison to DROID, BayesSim, and UDR.
A single task-agnostic trajectory of about 13 seconds was col-
lected through kinesthetic guidance and preprocessed in a sim-
ilar way to hockey puck—we used robot’s joint encoders to get
the joint positions and OptiTrack to track the object.
The converged DR distributions obtained from this data by
9


<!-- page 10 -->
DROPO
DROID
UDR
BayesSim
(MDRFF)
BayesSim
(MDNN)
0.0
2.5
5.0
7.5
10.0
12.5
15.0
Distance (cm)
Figure 12: Sim-to-real performance in terms of the ﬁnal distance to the target
position on the pushing setup (in centimeters; lower is better).
all benchmarked methods are presented in Table 4, averaged
over three seeds. Once again, we point out the smaller standard
deviations DROID converged to, compared to DROPO. How-
ever, as the real-world dynamics parameters are not known, the
ﬁnal evaluation has to be carried out by means of policy perfor-
mance on the real system, displayed in Figure 12 (5 rollouts per
policy, per seed).
In this task, DROPO consistently outperformed previous
methods and pushed the box as close as 2cm away from the
target location, showing another successful zero-shot transfer.
We observe how BayesSim, which resulted in less accurate pa-
rameter inference across our experiments, achieved inconsistent
performance and obtains similar results to DROID and UDR on
average. This result further motivated the need to infer dynam-
ics such as to account for both accurate system identiﬁcation
and domain randomization at the same time, even for a simple
pushing task. BayesSim with neural network features (MDNN)
predicted the box center of mass to be over 20 cm away from
the center in each direction, with a standard deviation of over
50cm, which results in the center of mass being located way
outside of the object. Like in the Hopper experiment with an
unmodeled phenomenon, this likely originates from the rather
poor generalization to real-world data, which lies outside of the
BayesSim network’s training distribution—consisting of simu-
lated data only. However, since the environment implementa-
tion clips the center of mass values to be within object bound-
aries, the agent was still able to learn a somewhat sensible pol-
icy for some random seeds. BayesSim with random Fourier
features (MDRFF) shows slightly better generalization to real
world data, producing a more sensible center of mass value, al-
beit with an excessive standard deviation of over 7cm in both
directions and (as visualized in the detailed results in Appendix
D.2) with negative mass being predicted on some occasions.
In terms of task performance, the trained policy still performs
worse on average than DROPO or DROID.
5. Conclusions
In this paper we introduced DROPO, a method for crossing
the reality gap by optimizing domain randomization distribu-
tions with limited, ofﬂine data. We demonstrated that, unlike
previous methods, DROPO is capable of accurately recovering
the dynamics parameter distributions used to generate a dataset
m
fx
fy
comx
comy
Search
space
min
0.08
0.20
0.20
-0.032
-0.032
max
2.00
2.00
2.00
0.032
0.032
Ground
truth
µ∗
0.7
0.8
0.8
0.01
0.01
σ∗
0.3
0.2
0.2
0.001
0.001
DROPO
ϵ=0
µ∗
0.788
0.603
0.683
0.015
0.009
σ∗
0.108
0.033
0.18
0.001
0.003
DROID
µ∗
0.774
0.737
0.716
0.014
0.011
σ∗
3.1e-11
1.3e-10
1.2e-11
7.6e-11
2.4e-11
BayesSim
µ∗
0.703
0.894
0.840
-0.011
0.004
σ∗
0.269
0.224
0.257
0.309
0.234
Table 3: Results of the sim-to-sim pushing task experiment with randomized
box mass m, table-box friction coefﬁcients ( fx, fy) and box center of mass in
meters (comx, comy).
m
fx
fy
comx
comy
Search
space
min
0.08
0.20
0.20
-0.032
-0.032
max
2.00
2.00
2.00
0.032
0.032
DROPO
ϵ=1e−4
µ∗
1.065
0.387
0.921
0.012
-0.032
σ∗
1.3e-04
3.0e-03
5.3e-04
5.2e-05
7.5e-04
DROID
µ∗
0.826
0.444
0.665
-0.028
-0.028
σ∗
1.4e-07
2.3e-08
2.6e-08
7.7e-08
6.6e-08
BayesSim
MDNN model
µ∗
1.548
3.889
0.964
-0.322
-0.240
σ∗
2.017
0.805
0.953
0.577
0.632
BayesSim
MDRFF model
µ∗
0.796
1.181
1.013
-0.023
-0.040
σ∗
0.252
0.218
0.316
0.090
0.075
Table 4: Optimized dynamics distributions on a single ofﬂine trajectory col-
lected on the real pushing environment. The converged box mass m, friction
coefﬁcients fx and fy, and box center of mass comx and comy (in meters) are
reported.
in simulation. We also showed how DROPO may compensate
for a misidentiﬁed value of a physical parameter, leading to
well-performing reinforcement learning policies in the target
domain.
We then moved on to real-world robotics setups—a hockey
puck sliding and a box pushing tasks. We demonstrated that a
policy trained in simulation with DROPO can be directly trans-
ferred to the real world on both setups, while previous methods
fail on the box pushing task. We conclude that our method is
able to effectively perform domain randomization and system
identiﬁcation at the same time, ﬁnding the right balance of pa-
rameter uncertainty by adjusting ϵ.
In the current work, we used a variety of data collection
strategies to collect the ofﬂine dataset—a partially-trained task
policy (Hopper), random sliding trajectories (Hockeypuck) and
human demonstrations obtained through kinesthetic teaching
(Pushing). Future works may investigate how the data collec-
tion strategy impacts the accuracy of parameters obtained by of-
ﬂine methods such as DROPO and DROID; in particular, prior
work on exploration in meta-learning would make an interest-
ing extension [37,38].
Under the current formulation, DROPO is limited to rela-
tively low-dimensional parametric distributions. This limita-
tion stems from the rather costly non-differentiable optimiza-
tion procedure; using less restrictive sampling procedures, such
as Stein variational gradient descent used in [22], could be a
promising way of further improving the accuracy. We showed
that DROPO is capable of performing optimization in up to
18-dimensional parameter spaces; while this was enough for
simple manipulation tasks, complex scenarios involving inter-
actions between multiple objects may involve many more pa-
10


<!-- page 11 -->
rameters, which could make DROPO prohibitively expensive.
Furthermore, in addition to larger dynamics parameter spaces,
we encourage future works to extend our method for likelihood
computation in high-dimensional state spaces, e.g. allowing
DROPO to work on vision-based policies and plain images col-
lected ofﬂine. In this case, the general idea behind DROPO
could be used not only to optimize the dynamics parameters
of the system, but also to adjust visual domain randomization
distributions for image rendering, for instance by adjusting pa-
rameters used for procedural generation of textures.
Domain randomization methods require the user not only to
specify the dynamics parameter distributions, but also to select
what parameters need to be randomized. In our experiments,
those parameters were indeed selected manually based on do-
main knowledge. While this approach works well with simple
and well-understood environments, it can present a challenge
in situations where expert knowledge of the application domain
is limited. Even though randomizing as much as possible may
appear to be a good idea on paper, it often leads to a signiﬁcant
increase in the computation cost. Additionally, some parameter
combinations may be physically impossible, leading to simula-
tor instabilities.
Aside from that, sim-to-real transfer with domain random-
ization often requires a signiﬁcant development effort, requir-
ing an accurate physics engine, object meshes and paramet-
ric simulation models to be available. As of now, there is no
automated way of designing simulation models that accurately
mimic real-world setups; such methods would make the initial
software development effort much lower, allowing sim-to-real
transfer with domain randomization to be used more widely in
the industry, for example in digital twin applications. Recent
developments in automated design open up the possibility of
automating the construction of simulation models beyond para-
metric inference. More speciﬁcally, the object shapes and the
general kinematic structure of the scene could be inferred based
on the appearance of the real world system, and have its dynam-
ics parameters tuned based on pre-collected physical observa-
tions using a method like DROPO.
Acknowledgment
This work was supported by Academy of Finland grants
317020 and 328399. We acknowledge the computational re-
sources generously provided by CSC – IT Center for Science,
Finland, and by the Aalto Science-IT project.
References
[1] V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wier-
stra, and M. Riedmiller, “Playing atari with deep reinforcement learn-
ing,” 2013.
[2] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. van den
Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanc-
tot, S. Dieleman, D. Grewe, J. Nham, N. Kalchbrenner, I. Sutskever,
T. Lillicrap, M. Leach, K. Kavukcuoglu, T. Graepel, and D. Hassabis,
“Mastering the game of Go with deep neural networks and tree search,”
Nature, vol. 529, pp. 484–489, January 2016.
[3] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep
reinforcement learning for robotics: a survey,” in IEEE Symposium Se-
ries on Computational Intelligence (SSCI), 2020.
[4] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and
V. Vanhoucke, “Sim-to-real: Learning agile locomotion for quadruped
robots,” in RSS, 2018.
[5] F. Sadeghi and S. Levine, “CAD2RL: real single-image ﬂight without a
single real image,” in Robotics: Science and Systems, 2017.
[6] A. H¨am¨al¨ainen, K. Arndt, A. Ghadirzadeh, and V. Kyrki, “Affordance
learning for end-to-end visuomotor robot control,” in IROS, 2019.
[7] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel,
“Domain randomization for transferring deep neural networks from sim-
ulation to the real world,” in IROS, 2017.
[8] F. Sadeghi, A. Toshev, E. Jang, and S. Levine, “Sim2real view invariant
visual servoing by recurrent control,” in CVPR, 2018.
[9] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-to-
real transfer of robotic control with dynamics randomization,” in ICRA,
2018.
[10] K. Arndt, M. Hazara, A. Ghadirzadeh, and V. Kyrki, “Meta reinforce-
ment learning for sim-to-real domain adaptation,” in ICRA, 2019.
[11] R. Antonova, S. Cruciani, C. Smith, and D. Kragic, “Reinforcement
learning for pivoting task,” 2017.
[12] A. Nagabandi, I. Clavera, S. Liu, R. S. Fearing, P. Abbeel, S. Levine,
and C. Finn, “Learning to adapt in dynamic, real-world environments
through meta-reinforcement learning,” in ICLR, 2019.
[13] M. Hazara and V. Kyrki, “Transferring generalizable motor primitives
from simulation to real world,” IEEE RA-L, vol. 4, 2019.
[14] OpenAI, “Learning dexterous in-hand manipulation,” IJRR, vol. 39,
2020.
[15] Y. Du, O. Watkins, T. Darrell, P. Abbeel, and D. Pathak, “Auto-tuned
sim-to-real transfer,” 2021.
[16] E. Valassakis, Z. Ding, and E. Johns, “Crossing the gap: A deep dive
into zero-shot sim-to-real transfer for dynamics,” in IROS, 2020.
[17] K. Arndt, A. Ghadirzadeh, M. Hazara, and V. Kyrki, “Few-shot model-
based adaptation in noisy conditions,” IEEE RA-L, 2021.
[18] A. Rajeswaran, S. Ghotra, B. Ravindran, and S. Levine, “EPOpt: Learn-
ing robust neural network policies using model ensembles,” 2017.
[19] F. Ramos, R. C. Possas, and D. Fox, “Bayessim: adaptive domain ran-
domization via probabilistic inference for robotics simulators,” 2019.
[20] Y.-Y. Tsai, H. Xu, Z. Ding, C. Zhang, E. Johns, and B. Huang, “Droid:
Minimizing the reality gap using single-shot human demonstration,”
IEEE Robotics and Automation Letters, vol. 6, no. 2, 2021.
[21] Y. Chebotar, A. Handa, V. Makoviychuk, M. Macklin, J. Issac, N. Ratliff,
and D. Fox, “Closing the sim-to-real loop: Adapting simulation random-
ization with real world experience,” in ICRA, 2019.
[22] B. Mehta, M. Diaz, F. Golemo, C. J. Pal, and L. Paull, “Active domain
randomization,” in CoRL, 2020.
[23] F. Muratore, C. Eilers, M. Gienger, and J. Peters, “Data-efﬁcient domain
randomization with bayesian optimization,” IEEE RA-L, vol. 6, 2021.
[24] S. Kolev and E. Todorov, “Physically consistent state estimation and sys-
tem identiﬁcation for contacts,” in 2015 IEEE-RAS 15th International
Conference on Humanoid Robots, IEEE, 2015.
[25] A. D. Allevato, E. Schaertl Short, M. Pryor, and A. L. Thomaz, “Iterative
residual tuning for system identiﬁcation and sim-to-real robot learning,”
vol. 44, no. 7, pp. 1167–1182, 2020.
[26] F. Muratore, M. Gienger, and J. Peters, “Assessing transferability from
simulation to reality for reinforcement learning,” IEEE Transactions on
Pattern Analysis and Machine Intelligence, 2019.
[27] F. de Avila Belbute-Peres, K. Smith, K. Allen, J. Tenenbaum, and J. Z.
Kolter, “End-to-end differentiable physics for learning and control,” in
NIPS, vol. 31, 2018.
11


<!-- page 12 -->
[28] N. Hansen and A. Ostermeier,
“Completely derandomized self-
adaptation in evolution strategies,” Evolutionary Computation, vol. 9,
no. 2, pp. 159–195, 2001.
[29] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Prox-
imal policy optimization algorithms,” 2017.
[30] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Off-
policy maximum entropy deep reinforcement learning with a stochastic
actor.,” in ICML, 2018.
[31] J. Rapin and O. Teytaud, “Nevergrad - A gradient-free optimization plat-
form,” 2018.
[32] G. Brockman, V. Cheung, L. Pettersson, J. Schneider, J. Schulman,
J. Tang, and W. Zaremba, “Openai gym,” 2016.
[33] A. Kumar, J. Fu, G. Tucker, and S. Levine, “Stabilizing off-policy q-
learning via bootstrapping error reduction,” 2019.
[34] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-
based control,” in IROS, 2012.
[35] A. Ghadirzadeh, A. Maki, D. Kragic, and M. Bj¨orkman, “Deep predic-
tive policy training using reinforcement learning,” in IROS, 2017.
[36] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of
deep visuomotor policies,” J. Mach. Learn. Res., vol. 17, Jan. 2016.
[37] K. Arndt, O. Struckmeier, and V. Kyrki, “Domain curiosity: Learning
efﬁcient data collection strategies for domain adaptation,” in IROS, 2021.
[38] J. Zhang, J. Wang, H. Hu, Y. Chen, C. Fan, and C. Zhang, “Learn to
effectively explore in context-based meta-rl,” in Arxiv, 2020.
[39] B. Mehta, A. Handa, D. Fox, and F. Ramos, “A user’s guide to calibrating
robotics simulators,” 2020.
[40] J. Peters, K. Muelling, and Y. Altun, “Relative entropy policy search,” in
AAAI, 2010.
Appendix A. Least squares for ofﬂine DR optimization
In this appendix section we attempt to give a more thor-
ough explanation to why DROID converged to point-estimate
dynamics parameters across all our experiments.
In partic-
ular, we aim to provide an intuition for why we discourage
the use of least squares-like methods for trajectory alignment
during ofﬂine optimization of DR distributions. This discus-
sion is further motivated by the results reported in [39], where
SimOpt’s [21] objective function was used in the ofﬂine set-
ting by replaying actions from off-policy data in simulation.
Similarly to our results with DROID, this approach resulted in
point-estimate dynamics estimates, leading the authors to con-
sider ofﬂine SimOpt as a point-estimate system identiﬁcation
method.
Based on the notation used throughout our work, let us con-
sider the optimization problem aiming to minimize the follow-
ing objective function:
J(ξ) = 1
K
K
X
i=1
∥f(si, ai; ξ) −si+1∥2
(A.1)
with f(·; ξ) being the simulator dynamics—assumed to be
deterministic for simplicity—parameterized by parameters ξ.
Note that, since the objective function is deﬁned for a given
dynamics parameter vector ξ, minimizing it by acting on the full
distribution is not straightforward. For example, DROID [20]
uses CMA to minimize the squared residuals and then re-
tains the ﬁnal inner CMA covariance matrix to ultimately build
the DR distribution. Similarly, SimOpt [21] uses a sampling-
based gradient-free algorithm based on relative entropy policy
search [40] allowing to minimize residuals using only samples
ξ ∼pφ(ξ).
Regardless of the speciﬁc method, since the ﬁnal goal is the
minimization of J(ξ), we can reason about its expected value
w.r.t. pφ(ξ), which we are ultimately interested in minimizing.
Intuitively, when optimizing the objective in (A.1) under no ad-
ditional assumptions or constraints, it is indeed reasonable to
believe that no beneﬁt is gained by ending up with a higher ex-
pected value of J(ξ) in exchange for a certain desired variance.
We then claim that optimization problems aiming to optimize
the expected value of quantity in A.1 by acting on the random
component itself, inevitably converge to point-estimates. Inter-
estingly enough, this draws similarities to the weighted average
of a ﬁnite sequence of numbers: no matter how you pick the
weights (e.g. the probability distribution), the average will al-
ways be greater than or equal to the minimum of the sequence;
only when moving all the probability mass to the minimum
value itself we get the lowest possible average value.
We attempt to give a concise mathematical demonstration
for this in our continuous case, under a few assumptions for
the sake of simplicity. Let us bound the search space of the
optimization problem to an arbitrary region in the dynamics
space. Let jmin = J(ξmin) be the global minimum of J(ξ) in
the region delimited by the support of the current pφ(ξ), poten-
tially trimmed by the predeﬁned search space in case of un-
bounded support.
Therefore, note how the random variable
Y = J(ξ) −jmin is always greater than or equal than zero. Fol-
lowing the non-negativity and linearity properties of expected
values, we consequently get:
E[Y] = E[J(ξ) −jmin] ⩾0
(A.2)
E[J(ξ)] ⩾jmin
(A.3)
This ﬁnal result indicates that regardless of how we design
the distribution pφ(ξ), we cannot do better than simply minimiz-
ing the objective function w.r.t. ξ only — indeed, we can only
do worse. Therefore, the optimization problem should converge
to the point-estimate ξmin even if acting on the full distribution,
assuming that our optimizer converges to the global minimum.
We then encourage future works to take these considerations
into account when designing optimization of dynamics distri-
butions with ﬁxed ofﬂine data. For example, one could add
custom constraints to promote variance in the dynamics param-
eters or, as shown by our work and BayesSim [19], move to
probabilistic metrics to infer target parameters.
Finally, it’s worth noting that these considerations do not ap-
ply to the original SimOpt method (as presented in [21]), as its
objective function is conceptually different in the online setting:
SimOpt optimizes φ so that a policy trained on such distribution
gets minimum squared residuals between its observed sim and
real states; i.e., the objective is directly to get a policy that per-
forms the same in both domains, as opposed to simple trajec-
tory alignment. Thus, having policy training and data collection
12


<!-- page 13 -->
from the real-world system in the loop prevents the optimiza-
tion from converging to a point estimate, as a policy trained on
a point estimate would—in most cases—fail to generalize to the
real world, resulting in a larger discrepancy between simulated
and real trajectories than a policy trained on a non-degenerate
dynamics distribution.
Appendix B. The impact of ϵ
To further analyze the impact of ϵ on DROPO’s performance
in presence of noise, we performed a secondary analysis where
we corrupt the collected Hopper datasets with different levels
of noise.
The results for the point-dynamics Hopper dataset described
in Section 4.2.1 are depicted in Figure B.13. In line with the
main experimental evaluation, we observed a consistent drop
in MSE where ϵ matches the noise level σ2. In addition, the
results in terms of the converged mean (Figure B.13b) are con-
sistent for ϵ ≥σ2, and the standard deviations are very low,
corresponding to a correct identiﬁcation of point dynamics pa-
rameters.
We ﬁnally performed a similar analysis for the distribution
recovery case, which produced similar results: the dynamics
distribution recovery is most accurate at ϵ close to the noise
variance σ2, which also corresponds to the sharp drop in MSE.
In particular, note how the converged standard deviations of the
four masses resemble the ground truth distributions deﬁned in
Section 4.2.2, as long as ϵ does not increase to overly large
values w.r.t. the current noise level.
Appendix C. Sensitivity to the amount of data
As observed in our experiments section, DROPO succeeded
to transfer RL pushing policies to the real world with as little
as a single demonstrative trajectory for parameter inference. In
this section, we aim to quantify the sensitivity of DROPO to the
amount of ofﬂine data collected. To this end, we analyzed the
converged means of the dynamics distributions with different
amount of state transitions in different noise levels, for the Hop-
per environment in the point-dynamics setting of Section 4.2.1.
In particular, we tested DROPO with 10, 30, 100, 300, 1000
and 3000 state transitions sub-sampled from the ofﬂine dataset,
and kept ϵ ﬁxed at the value of 10−5. We report the conﬁdence
interval of the converged mean of each mass of the Hopper in
Fig. C.15, obtained from 4 runs for each evaluation.
We observe that, when noise variance is around 10−8 or
lower, as little as 10 state transitions are enough for DROPO
to converge to values very close to the ground truth values. For
higher noise levels, this number increases to several hundreds
of state transitions. However, note the relatively small scale on
the y-axis, where conﬁdence intervals get as wide as 10 grams
at most.
For the sake of clarity, we ﬁnally combine and report in Ta-
ble B.5 the amount of data used in all our experiments. Target
data has been collected in less than a minute of interaction for
all tasks, motivating the adoption of ofﬂine DR optimization
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
MSE in Hopper
10
11
10
9
10
7
10
5
10
3
10
1
(a)
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Torsomass
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Thighmass
1.0
1.5
2.0
2.5
3.0
3.5
4.0
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Legmass
1.0
1.5
2.0
2.5
3.0
3.5
4.0
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Footmass
2
3
4
5
6
Hopper distribution means
(b)
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Torsomass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Thighmass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Legmass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Footmass
10
5
10
4
10
3
10
2
10
1
100
Hopper distribution standard devs
(c)
Figure B.13: Relationship between noise level, epsilon and the resulting (a)
MSE and (b, c) distribution, expressed by mean and standard deviation in the
Hopper point-dynamics system identiﬁcation case. (results averaged over 4
random seeds)
13


<!-- page 14 -->
Experiment
Number of
trajectories
Transitions
per trajectory
Time per
transition
Total
transitions
Total
time
Hopper
2
500
8ms
1000
8s
Hockeypuck
5
750
10ms
3750
37.5s
Sim-to-sim push
50
30
20ms
1500
30s
Sim-to-real push
1
1286
10ms
1286
12.86s
Table B.5: The amount of data used for each experiment, broken down into trajectories, state transitions, and the total time.
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
MSE in Hopper
10
4
10
3
10
2
10
1
(a)
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Torsomass
1.0
1.5
2.0
2.5
3.0
3.5
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Thighmass
1
2
3
4
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Legmass
1
2
3
4
5
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Footmass
1
2
3
4
5
Hopper distribution means
(b)
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Torsomass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Thighmass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Legmass
10
5
10
4
10
3
10
2
10
1
100
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Noise variance
1e-10
1e-09
1e-08
1e-07
1e-06
1e-05
0.0001
0.001
0.01
0.1
Epsilon
Footmass
10
5
10
4
10
3
10
2
10
1
100
Hopper distribution standard devs
(c)
Figure B.14: Relationship between noise level, epsilon and the resulting (a)
MSE and the (b, c) distribution, expressed by mean and standard deviation in
the Hopper dynamics distribution recovery case. (results averaged over 4 ran-
dom seeds)
101
102
103
Number of state transitions
3.51
3.52
3.53
3.54
3.55
torsomass:_mean
Torsomass
noise
0.0
1e-10
1e-08
1e-06
101
102
103
Number of state transitions
3.91
3.92
3.93
3.94
3.95
3.96
thighmass:_mean
Thighmass
noise
0.0
1e-10
1e-08
1e-06
101
102
103
Number of state transitions
2.67
2.68
2.69
2.70
2.71
2.72
legmass:_mean
Legmass
noise
0.0
1e-10
1e-08
1e-06
101
102
103
Number of state transitions
5.06
5.08
5.10
5.12
5.14
5.16
5.18
footmass:_mean
Footmass
noise
0.0
1e-10
1e-08
1e-06
Hopper distribution means
Figure C.15: Hopper dynamics parameter estimated mean with its 95% conﬁ-
dence interval (estimated by bootstrapping over 4 random seeds)
for critical-to-operate environments. Noticeably more data has
been used to infer dynamics for the Hockeypuck environment,
due to the nature of the task and the robot arm moving through
the air before hitting the hockey puck, with the puck moving
only for about a second in each trajectory (thus, only a small
subset of state transitions could be used to infer the dynamics
of the hockey puck).
Appendix D. Complete BayesSim results
BayesSim parameterizes the resulting dynamics distributions
as a mixture of multivariate Gaussians, while other methods
used simple Gaussian distributions. In order to clearly present
the inferred distributions in comparison with the other meth-
ods in the Experiments section of the paper, we simpliﬁed the
BayesSim results by only reporting the diagonal uncorrelated
approximation of the Gaussian mixture. While this gives a good
intuition about the accuracy of the results, it loses some of the
information; hence, we here provide plots of the full mixture
Gaussian distributions.
In this section, we provide the full BayesSim inference re-
sults by plotting histograms and joint distributions over all pairs
of dynamics parameters. Each color corresponds to an indepen-
dent training run of the BayesSim inference network.
Appendix D.1. Hopper
Here, we present the complete dynamics estimation results in
Hopper. The ground-truth values for the point dynamics recov-
ery experiment were reported in Table 1 and for the dynamics
distribution recovery in Figure 3.
14


<!-- page 15 -->
The parameters (from param0 to param3) represent the
masses of consecutive Hopper links—torso, thigh, leg and foot.
In the unmodeled phenomenon experiment (Figure D.18), the
torso mass is excluded as it is ﬁxed to an incorrect value and
is not inferred during optimization. In this case, as previously
argued, the test environment does not lie within the distribution
of environments used for training data generation. As a result,
the evaluation data lies outside of the training domain of the
BayesSim inference network. This is likely the reason why the
network produces a distribution with a large standard deviation
centered around the mean of the search bounds.
We observe that in all distribution recovery experiments,
BayesSim correctly returns a mixture model that is effectively
a unimodal Gaussian distribution (with the weights of the re-
maining mixture components very close to zero).
In Figure D.17, we also observed a signiﬁcant discrepancy
between different repetitions of the experiment, i.e. indepen-
dent training runs of the BayesSim inference network.
0.0
0.2
0.4
0.6
0.8
1.0
param0
10
0
10
20
param1
5
0
5
10
param2
2.5
0.0
2.5
5.0
param0
0
5
10
15
param3
10
0
10
20
param1
5
0
5
10
param2
0
5
10
15
param3
Figure D.16:
Complete dynamics identiﬁcation results in Hopper with
BayesSim
0.0
0.2
0.4
0.6
0.8
1.0
param0
4.0
4.5
5.0
param1
2.00
2.25
2.50
2.75
3.00
param2
2.8
3.0
3.2
3.4
param0
4.5
5.0
5.5
param3
4.0
4.5
5.0
param1
2.0
2.5
3.0
param2
4.5
5.0
5.5
param3
Figure D.17: Complete dynamics distribution recovery results in Hopper with
BayesSim
0.0
0.2
0.4
0.6
0.8
1.0
param0
2.5
0.0
2.5
5.0
7.5
param1
0
5
10
param0
2.5
0.0
2.5
5.0
7.5
10.0
param2
0
5
param1
0
5
10
param2
Figure D.18: Complete dynamics estimation results in Hopper with unmodeled
phenenomena with BayesSim
Appendix D.2. Panda
Here, we present the full BayesSim results for the Panda
pushing task. The estimated dynamics parameters are, in or-
der, the mass of the box, the friction coefﬁcient values along
axes x and y, and the x and y position of center of mass of the
box.
15


<!-- page 16 -->
0.0
0.2
0.4
0.6
0.8
1.0
param0
0.0
0.5
1.0
1.5
2.0
param1
0
1
2
param2
1
0
1
2
param3
1
0
1
param0
1
0
1
param4
0
1
2
param1
0
1
2
param2
0
2
param3
1
0
1
param4
Figure D.19: Complete dynamics distribution recovery results in Panda with
BayesSim
In the sim-to-sim inference experiment (Figure D.19) we ob-
serve that, despite there being some variance between random
seeds, the models generally agree that the center of mass along
x and y should be shifted in the positive direction, and that the
mass of the object is rather hard to identify (as expressed by the
large standard deviation for param0).
However, when operating on real-world data, the model’s
performance degrades signiﬁcantly, especially with the neural
network features (MDNN), shown in Figure D.20. In this case,
the model produces very large standard deviations, potentially
hindering the training process and often leading to unfeasible
physical parameters—e.g. negative masses or box center of
mass that lies outside the box boundaries. To address this is-
sue, all values were clipped inside the simulator and kept within
the pre-identiﬁed search space, which made the policy train-
ing possible. Like in the unmodeled Hopper experiment, we
suspect that this behaviour is the result of the network being
evaluated on out-of-distribution data. This hypothesis appears
stronger when looking at the results obtained with the quasi-
random Fourier features, where the inferred distributions look
more sensible, although in some cases the mixture components
still predict the mass to be negative (Figure D.21). The feature
extraction process reduces the dimensionality of the input data,
making it easier for the model to generalize to new data, as it
is more likely that the noisy, unmodeled real-world trajectory
would appear close to data seen during training.
0.0
0.2
0.4
0.6
0.8
1.0
param0
0
2
4
6
8
param1
2.5
0.0
2.5
5.0
7.5
param2
4
2
0
2
param3
10
0
10
param0
4
2
0
2
4
param4
0
5
param1
0
5
param2
5.0
2.5
0.0
2.5
param3
2.5
0.0
2.5
param4
Figure D.20: Complete real-world dynamics estimation results in Panda with
BayesSim (MDNN features)
0.0
0.2
0.4
0.6
0.8
1.0
param0
0.0
0.5
1.0
1.5
param1
0
1
2
param2
0.4
0.2
0.0
0.2
param3
0
1
2
param0
0.4
0.2
0.0
0.2
param4
0
1
param1
0
1
2
param2
0.4
0.2
0.0
0.2
param3
0.2
0.0
0.2
param4
Figure D.21: Complete real-world dynamics estimation results in Panda with
BayesSim (MDRFF features)
16
