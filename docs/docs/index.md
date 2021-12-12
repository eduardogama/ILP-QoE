# Introduction to MLFLP

The Multi-level facility location problem (MLFLP) is a Capacited Facility Problem's branch in which is a basic optimization problem, where the total demand that each facility may satisfy is limited. The MLFLP is encoutered in supply chains and production-distribution systems. Inside this context  there exist an inherent hierarchy given by the nature of the system and a successively exclusive facility hierarchy is usually considered. Hence, modeling such problem must take into account both demand satisfaction and capacity constraints.

To illustrate one example of the MLFLP, in the case of production-distribution systems, the products need to be first produced in order to be shipped to regional warehouses for temporary storage. 

[...]

## Appendix A

The capacitated facility location problem (CFLP) is the basis for many practical optimization problems, where the total demand that each facility may satisfy is limited. Hence, modeling such problem must take into account both demand satisfaction and capacity constraints.

Let us start with a concrete example. Consider a company with three potential sites for installing its facilities/warehouses and five demand points. Each site $j$ has a yearly activation cost $f_{j}$, i.e., an annual leasing expense that is incurred for using it, independently of the volume it serves. This volume is limited to a given maximum amount that may be handled yearly, $M_{j}$. Additionally, there is a transportation cost $c_{ij}$ per unit served from facility $j$ to the demand point $i$. 

Let us formulate the problem as a mathematical optimization model. Consider $n$ customers $i = 1,2,...,n$ and $m$ sites for facilities $j=1,2,...,m$. Define continuous variables $x_{ij} \geq 0$ as the amount serviced from facility $j$ otherwise. An integer-optimization model for the capacitated facility location problem can now be specified as follows:

minimize

\begin{equation}
\sum^{m}_{j=1} f_{j}y_{j} + \sum^{n}_{i=1}\sum^{m}_{j=1} c_{ij}x_{ij} \label{eq:result}
\end{equation}

Subject to

$$
\sum^{m}_{j=1} x_{ij} = d_{i} \text{ } \forall i = 1,...,n 
$$

$$
\sum^{n}_{i=1} x_{ij} \leq M_{j}y_{j} \text{ } \forall j = 1,...,m
$$

$$
x_{ij} \leq d_{i}y_{j} \text{ } \forall i = 1,...,n; \forall j = 1,...,m
$$

$$
x_{ij} \geq 0 \text{ } \forall i = 1,...,n; \forall j = 1,...,m
$$

$$
y_{j} \in \{0,1\} \text{ } \forall j = 1,...,m
$$


The objective of the problem is to minimize the sum of facility activation costs and transportation costs. The first constraints require that each customer’s demand must be satisfied. The capacity of each facility $j$ is limited by the second constraints: if facility $j$ is activated, its capacity restriction is observed;  if it is not activated, the demand satisfied by $j$ is zero.



