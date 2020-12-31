# csv列定义

0. line_offset\[int\]: 评论在原文件中相对于0的行
1. asin\[char(10)\]: 亚马逊asin号
2. user_id\[varchar()\]: 用户ID，一般9位到14位，或者oc-*****的格式，会很长
3. profile_name\[varchar\]: 用户名
4. helpfulness_numerator\[integer\]: 觉得该评论有用的人数
5. helpfulness_denominator\[integer\]: 对该评论评分的人数(比上面一个大)
6. score\[float\]: 打分[0.0~5.0]
7. time[\int\]: 时间戳
8. summary\[varchar\]: 评论总结
9. polarity\[float\]: 情感评分的极性，\[-1. 1\]之间，1代表正面，-1代表负面
10. subjectivity\[float\]: 主观性的评分，\[0, 1]之间，1代表主观，0代表客观