import re

class VerilogAssign:
    def __init__(self, assign_str=""):
        self.assign_str = assign_str
        self.ports = []  # 输入和输出端口（包含位宽）
        self.wires = []  # 所有变量（包含位宽）
        
        if assign_str:
            self.parse_assign(assign_str)
    
    def parse_assign(self, assign_str):
        """解析assign语句，提取变量名和位宽信息"""
        self.assign_str = assign_str.strip()
        
        # 提取左右两部分
        match = re.match(r"assign\s+(.+?)\s*=\s*(.+?)\s*;", self.assign_str)    
        if not match:
            raise ValueError("Invalid assign statement format")
        
        left, right = match.groups()
        
        # 处理左侧（输出）
        output_var = self._extract_var_with_width(left)
        if output_var not in self.ports:
            self.ports.append(output_var)
        if output_var not in self.wires:
            self.wires.append(output_var)
        
        # 处理右侧（输入和可能的中间变量）
        input_vars = self._extract_vars_with_widths_ignore_constants(right)
        for var in input_vars:
            if var not in self.wires:
                self.wires.append(var)
            # 如果变量不在ports中且不是输出变量，则添加到ports（作为输入）
            if var not in self.ports and var != output_var:
                self.ports.append(var)
    
    def _extract_var_with_width(self, expr):
        """从表达式中提取变量名和位宽信息，忽略拼接操作符{}"""
        # 先处理拼接操作中的各个部分
        if expr.startswith('{') and expr.endswith('}'):
            # 去掉大括号，分割各部分
            parts = expr[1:-1].split(',')
            # 理论上左侧拼接的应该是wire/reg，这里简单处理
            # 实际应用中可能需要更复杂的处理
            return [self._extract_single_var(part.strip()) for part in parts]
        return self._extract_single_var(expr)
    
    def _extract_single_var(self, expr):
        """提取单个变量（可能带位宽）"""
        # 匹配变量名和可能的位宽，排除数字常量
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)(\[.*?\])?$", expr.strip())
        if not match:
            return None
        var_name, width = match.groups()
        return f"{var_name}{width}" if width else var_name
    
    def _extract_vars_with_widths_ignore_constants(self, expr):
        """从表达式中提取所有变量及其位宽信息，忽略常量"""
        # 先处理拼接操作
        if expr.startswith('{') and expr.endswith('}'):
            inner_expr = expr[1:-1]
            parts = [part.strip() for part in inner_expr.split(',')]
            vars_in_concatenation = []
            for part in parts:
                if self._is_constant(part):
                    continue
                var = self._extract_single_var(part)
                if var:
                    vars_in_concatenation.append(var)
            return vars_in_concatenation
        
        # 处理普通表达式
        # 匹配变量名（可能带位宽），排除常量
        pattern = r"\b([a-zA-Z_][a-zA-Z0-9_]*)(\[.*?\])?\b(?!\s*'[bdh])"
        matches = re.finditer(pattern, expr)
        
        variables = []
        for match in matches:
            var_name, width = match.groups()
            # 排除Verilog关键字
            if var_name.lower() in [
                "and", "or", "not", "nand", "nor", "xor", "xnor",
                "assign", "input", "output", "wire", "reg"
            ]:
                continue
            # 组合变量名和位宽
            var_with_width = f"{var_name}{width}" if width else var_name
            variables.append(var_with_width)
        
        return variables
    
    def _is_constant(self, expr):
        """判断是否是常量（数字或Verilog常量表示）"""
        # 匹配数字常量：4'b0, 8'hFF, 3'd5, 16等
        const_pattern = r"^\d+['bdh][0-9a-fA-F_xzXZ]+$|^\d+$|^[01]+$"
        return re.match(const_pattern, expr) is not None
    
    def __str__(self):
        return (f"VerilogAssign: {self.assign_str}\n"
                f"Ports: {self.ports}\n"
                f"Wires: {self.wires}")


# 示例用法
if __name__ == "__main__":
    # 示例1：简单assign语句
    assign1 = "assign out = in1 & in2;"
    va1 = VerilogAssign(assign1)
    print(va1)
    
    # 示例2：带有位选择和常量的assign语句
    assign2 = "assign data_out[7:0] = {data_in[3:0], 4'b0};"
    va2 = VerilogAssign(assign2)
    print("\n", va2)
    
    # 示例3：复杂表达式
    assign3 = "assign result[15:0] = (temp1[7:0] | temp2[3:0]) & enable;"
    va3 = VerilogAssign(assign3)
    print("\n", va3)
    
    # 示例4：混合情况
    assign4 = "assign {out1[3:0], out2} = {in1[1:0], in2, 2'b00};"
    va4 = VerilogAssign(assign4)
    print("\n", va4)
    
    # 示例5：包含多个常量
    assign5 = "assign flag = (state == 3'b001) & (count > 5);"
    va5 = VerilogAssign(assign5)
    print("\n", va5)