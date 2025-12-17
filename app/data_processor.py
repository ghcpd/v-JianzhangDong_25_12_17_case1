class DataProcessor:
    # Missing doc 3: 类缺少docstring

    def __init__(self, data: list):
        """初始化数据处理器"""
        self.data = data

    def normalize(self) -> list:
        """对数据进行归一化"""
        max_val = max(self.data)
        min_val = min(self.data)
        return [(x - min_val) / (max_val - min_val) for x in self.data]
