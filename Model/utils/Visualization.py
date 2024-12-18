class Heatmap:
    # 对进化过程中个体的fitness值进行可视化
    def __init__(self, model, data, device):
        self.model = model
        self.data = data
        self.device = device


        
class DR:
    # 尝试一个UMAP降维分析:以12个不同的fitness函数值组成向量,观察不同fitness评价指标下完成迭代时的个体分布
    def __init__(self, model, data, device):
        self.model = model
        self.data = data
        self.device = device

    def run(self):
        pass