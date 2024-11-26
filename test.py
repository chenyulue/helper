from dataclasses import dataclass
import re

@dataclass
class Claim:
    number: int
    dependency: list[int]
    is_dependent: bool
    title: str
    content: str
    start_pos: int

def parse_claims(text):
    claims = []
    claim_pattern = re.compile(r'(\d+)\.\s+(.+?)(?=\s*\d+\.\s+|$)', re.DOTALL)
    
    for match in claim_pattern.finditer(text):
        number = int(match.group(1))
        content = match.group(2).strip()
        start_pos = match.start(0)
        
        # Determine if the claim is dependent
        if content.startswith("根据"):
            is_dependent = True
            dependency_match = re.search(r'根据权利要求(\d+)所述', content)
            dependency = [int(dependency_match.group(1))] if dependency_match else []
        else:
            is_dependent = False
            dependency = []
        
        # Extract the title (text before the first comma)
        title_match = re.search(r'(.*?),', content)
        title = title_match.group(1) if title_match else content
        
        claim = Claim(number=number, 
                      dependency=dependency, 
                      is_dependent=is_dependent, 
                      title=title, 
                      content=content, 
                      start_pos=start_pos)
        claims.append(claim)
    
    return claims

# 示例权利要求书
claims_text = """
1. 一种新型节能照明系统，其特征在于，包括：
一个中央控制器（1）；
多个与中央控制器（1）无线连接的节能灯具（2）；
其中，中央控制器（1）配置有控制算法，用于根据环境光线强度自动调节灯具（2）的亮度。
2. 根据权利要求1所述的新型节能照明系统，其特征在于，所述中央控制器（1）还配置有用户界面，允许用户手动设置灯具（2）的亮度和颜色。
3. 一种控制新型节能照明系统的方法，其特征在于，包括以下步骤：
步骤A：检测环境光线强度；
步骤B：根据检测到的环境光线强度，自动调节灯具的亮度；
步骤C：通过中央控制器的用户界面接收用户输入，手动调整灯具的亮度和颜色。
4. 根据权利要求3所述的方法，其特征在于，还包括一个步骤D：在检测到特定环境事件时，自动改变灯具的颜色以提醒用户。
5. 根据权利要求3所述的方法，其特征在于，所述自动调节灯具亮度的步骤B中，还包括一个子步骤B1：根据预设的节能模式，调整灯具的亮度以优化能源消耗。
"""

parsed_claims = parse_claims(claims_text)

for claim in parsed_claims:
    print(f"Number: {claim.number}")
    print(f"Dependency: {claim.dependency}")
    print(f"Is Dependent: {claim.is_dependent}")
    print(f"Title: {claim.title}")
    print(f"Content: {claim.content}")
    print(f"Start Pos: {claim.start_pos}\n")



