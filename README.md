# My thesis
My Thesis Knowledge Graph Embedding for Link Prediction

Contributor:
* [Phan Minh Tâm](https://github.com/MinhTamPhan)  - phanminhtam247@gmail.com
* [Hoàng Minh Thanh](https://github.com/hmthanh) - hmthanhgm@gmail.com

## Our Contribution:


[Our thesis - vietnamese version](./Thesis_Link_Prediction_final.pdf)

[english version](./) update later(submiting)

### We Contribution in rule base AnyBURL:
- strategy offline-to-online adding knowledge into graph.
- strategy online-to-online adding knowledge into graph.

### We Contribution in deep learning method:
- apply Attention Mechanism into knowledge graph.
- implement and evaluation KBGAT.

## Our result
|         | FB15K |       | FB15K-237 |       |  WN18 |       | WN18RR |       |
|---------|:-----:|:-----:|:---------:|:-----:|:-----:|:-----:|:------:|-------|
|         | H@1   | H@10  | H@1       | H@10  | H@1   | H@10  | H@1    | H@10  |
| AnyBURL | 79.13 | 82.30 | 20.85     | 42.40 | 93.96 | 95.07 | 44.22  | 54.40 |
| CGAT    | *     | *     | 36.06     | 58.32 | *     | *     | 35.12  | 57.01 |

## [source-anyburl](./source/README.md)
* fully testing 4 data set [fully_testing.ipynb](./AnyBURL/fully_testing.ipynb)
* learn with strategy offline-to-online adding knowledge into graph. [learning_extend_rule.ipynb](./AnyBURL/learning_extend_rule.ipynb)
* strategy online-to-online adding knowledge into graph. [learning_extend_rule.ipynb](./AnyBURL/learning_with_edge.ipynb)
## [source-CGAT](./source/README.md)
* [FB15k_237.ipynb](GCAT_FB15k_237.ipynb)
* [GCAT_FB15k.ipynb](GCAT_FB15k.ipynb)
* [GCAT_WN18.ipynb](GCAT_WN18.ipynb)
* [GCAT_WN18RR.ipynb](GCAT_WN18RR.ipynb)