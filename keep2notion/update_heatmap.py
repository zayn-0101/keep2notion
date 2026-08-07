import os
from keep2notion.utils import get_embed
from keep2notion.notion_helper import NotionHelper


def main():
    source_dir = "OUT_FOLDER"
    if not os.path.isdir(source_dir):
        print("OUT_FOLDER does not exist.")
        return
    files = [f for f in os.listdir(source_dir) if f.endswith(".svg")]
    if not files:
        print("未生成运动热力图，跳过更新")
        return
    # workflow 已把 notion.svg 重命名为随机名并提交到仓库，取唯一的 svg
    image_file = files[0]
    repository = os.environ["REPOSITORY"]
    branch = os.getenv("ARTIFACT_BRANCH", "main")
    relative_root = os.getenv("NOTIONHUB_ARTIFACT_PATH", "OUT_FOLDER").strip("/")
    heatmap_url = (
        f"https://raw.githubusercontent.com/{repository}/{branch}/"
        f"{relative_root}/{image_file}"
    )
    if notion_helper.heatmap_block_id:
        notion_helper.update_heatmap(
            block_id=notion_helper.heatmap_block_id, url=heatmap_url
        )
    else:
        # 页面还没有热力图块，自动创建一个 embed 块
        notion_helper.append_blocks(
            block_id=notion_helper.page_id,
            children=[get_embed(heatmap_url)],
        )


notion_helper = NotionHelper()
