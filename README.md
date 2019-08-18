# Wikipedia-Hyperlink-Graph

In this project we perform an analysis of the Wikipedia Hyperlink graph. In particular, given extra information about the categories to which an article belongs to, we are curious to rank the articles according to some criteria. 

For this purpose we use the Wikipedia graph released by the SNAP group.

<div style="text-align:center"><img src ="https://cryptobriefing.com/wp-content/uploads/2018/04/Wikipedia-and-Request-Network-enable-donors-to-donate-in-cryptocurrency.jpg" /></div>

***

## Research questions

<div style="text-align:center"><img src ="http://allywebs.com/images/social_networking.png" /></div>

**[RQ1]** Build the graph <img src="https://latex.codecogs.com/gif.latex?G=(V,&space;E)" title="G=(V, E)" />, where *V* is the set of articles and *E* the hyperlinks among them, and provide its basic information:
 
- If it is direct or not
- The number of nodes
- The number of edges 
- The average node degree. Is the graph dense?

**[RQ2]** Given a category <img src="https://latex.codecogs.com/gif.latex?C_0&space;=&space;\{article_1,&space;article_2,&space;\dots&space;\}" title="C_0 = \{article_1, article_2, \dots \}" /> as input we want to rank all of the nodes in *V* according to the following criteria:
	
* Obtain a *block-ranking*, where the blocks are represented by the categories. In particular, we want:


<img src="https://latex.codecogs.com/gif.latex?block_{RANKING}&space;=\begin{bmatrix}&space;C_0&space;\\&space;C_1&space;\\&space;\dots&space;\\&space;C_c\\&space;\end{bmatrix}" title="block_{RANKING} =\begin{bmatrix} C_0 \\ C_1 \\ \dots \\ C_c\\ \end{bmatrix}" />
	
Each category <img src="https://latex.codecogs.com/gif.latex?C_i"/> corresponds to a list of nodes. 


![alt text](imgs/sort_inside_categories.png)

The first category of the rank, <img src="https://latex.codecogs.com/gif.latex?C_0" title="C_0" />, always corresponds to the input category. The order of the remaining categories is given by:



<img src="https://latex.codecogs.com/gif.latex?$$distance(C_0,&space;C_i)&space;=&space;median(ShortestPath(C_0,&space;C_i))$$" title="distance(C_0, C_i) = median(ShortestPath(C_0, C_i))" />

The lower is the distance from <img src="https://latex.codecogs.com/gif.latex?C_0" title="C_0" />, the higher is the <img src="https://latex.codecogs.com/gif.latex?C_i" title="C_i" /> position in the rank. <img src="https://latex.codecogs.com/gif.latex?ShortestPath(C_0,&space;C_i)" title="ShortestPath(C_0, C_i)" /> is the set of all the possible shortest paths between the nodes of <img src="https://latex.codecogs.com/gif.latex?C_0" title="C_0" />  and <img src="https://latex.codecogs.com/gif.latex?C_i" title="C_i" />. Moreover, the length of a path is given by the sum of the weights of the edges it is composed by.


* Once you obtain the <img src="https://latex.codecogs.com/gif.latex?block_{RANKING}" title="block_{RANKING}" /> vector, you want to sort the nodes in each category. The way you should sort them is explained by this example:

	*	Suppose the categories order, given from the previous point, is <img src="https://latex.codecogs.com/gif.latex?C_0,&space;C_1,&space;C_2" title="C_0, C_1, C_2" />


__[STEP1]__ Compute subgraph induced by <img src="https://latex.codecogs.com/gif.latex?C_0" title="C_0" />. For each node compute the sum of the weigths of the in-edges.

 <img src="https://latex.codecogs.com/gif.latex?score_{article_i}&space;=&space;\sum_{i&space;\in&space;in-edges}&space;w_i" title="score_{article_i} = \sum_{j \in in-edges(article_i)} w_j" />

__[STEP2]__ Extend the graph to the nodes that belong to <img src="https://latex.codecogs.com/gif.latex?C_1" title="C_1" />. Thus, for each article in <img src="https://latex.codecogs.com/gif.latex?C_1" title="C_1" /> compute the score as before. __Note__ that the in-edges coming from the previous category, <img src="https://latex.codecogs.com/gif.latex?C_0" title="C_0" />, have as weights the score of the node that sends the edge.


__[STEP3]__ Repeat Step2 up to the last category of the ranking. In the last step of the example you clearly see the weight update of the edge coming from node *E*.
	
![alt text](imgs/algorithm.png)
