import re

def txt_to_latex(input_file, output_file):
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式分割章节（处理可能存在的空格和换行）
    chapter_pattern = r'(第[\d零一二三四五六七八九十百千]+章\s*[^\n]+)'
    chapters = re.split(chapter_pattern, content)
    
    # 创建LaTeX文档头部
    name=input("请输入小说名称：");
    man=input("请输入作者名称：");
    latex_content = [
        r'\documentclass[UTF8, fontset=windows, xelatex]{ctexart}',
        #ds说使用这个快一点，其实我也不太清楚QAQ
        r'\usepackage[top=2cm, bottom=2cm, left=2.5cm, right=2.5cm]{geometry}',
        r'\usepackage{parskip}',
        r'\special{dvipdfmx:config z 0}',#这一行是用来组织pdf文件压缩的，编译快一点
        r'\setlength{\parindent}{2em}',
        r'\title{'+name+'}',
        r'\author{'+man'}',
        r'\date{\today}',
        r'\begin{document}',
        r'\maketitle',
        r'\tableofcontents',
        r'\newpage'
    ]
    
    # 处理每个章节
    for i in range(1, len(chapters)):
        if i % 2 == 1:  # 奇数索引是章节标题
            chapter_title = chapters[i].strip()
            
            # 获取章节内容（下一个元素）
            chapter_content = chapters[i+1] if i+1 < len(chapters) else ''
            
            # 添加章节标题
            latex_content.append(f'\\section{{{chapter_title}}}')
            
            # 提取所有段落
            paragraphs = []
            start_index = 0
            
            # 使用正则表达式查找所有段落
            para_matches = list(re.finditer(r'<p class="bodyContent-1">', chapter_content))
            
            for j, match in enumerate(para_matches):
                start_pos = match.end()
                
                # 查找下一个段落开始位置或章节结束
                if j < len(para_matches) - 1:
                    end_pos = para_matches[j+1].start()
                else:
                    end_pos = len(chapter_content)
                
                # 提取段落内容
                para_text = chapter_content[start_pos:end_pos]
                
                # 移除可能存在的HTML标签和多余空格
                cleaned_para = re.sub(r'</?p[^>]*>', '', para_text)  # 移除任何<p>或</p>标签
                cleaned_para = re.sub(r'<[^>]+>', '', cleaned_para)  # 移除其他HTML标签
                cleaned_para = re.sub(r'\s+', ' ', cleaned_para).strip()  # 合并多余空格
                
                # 跳过空段落
                if not cleaned_para:
                    continue
                
                paragraphs.append(cleaned_para)
            
            # 添加段落内容到LaTeX
            for para in paragraphs:
                # 转义特殊字符
                for char in ['&', '%', '$', '#', '_', '{', '}', '~', '^', '\\']:
                    para = para.replace(char, f'\\{char}')
                
                # 处理中文引号
                para = para.replace('“', r'``').replace('”', r"''")
                
                # 添加到LaTeX内容
                latex_content.append(para)
                latex_content.append('')  # 添加空行实现段落间距
    
    # 添加文档尾部
    latex_content.append(r'\end{document}')
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))

# 使用示例
if __name__ == "__main__":
    input_filename = 'test.txt'   # 输入文件名
    output_filename = "novel.tex"  # 输出文件名
    txt_to_latex(input_filename, output_filename)