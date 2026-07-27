import os
import shutil
from keep2notion.notion_helper import NotionHelper

def main():
    source_path = os.path.abspath("OUT_FOLDER/notion.svg")
    if not os.path.exists(source_path):
        print("未生成运动热力图，跳过更新")
        return
    artifact_root = os.getenv(
        "NOTIONHUB_ARTIFACT_ROOT",
        os.path.abspath(".notionhub-artifacts/keep"),
    )
    os.makedirs(artifact_root, exist_ok=True)
    target_path = os.path.join(artifact_root, "workout.svg")
    shutil.move(source_path, target_path)
    repository = os.environ["REPOSITORY"]
    branch = os.getenv("ARTIFACT_BRANCH", "main")
    relative_root = os.getenv(
        "NOTIONHUB_ARTIFACT_PATH",
        ".notionhub-artifacts/keep",
    ).strip("/")
    heatmap_url = (
        f"https://raw.githubusercontent.com/{repository}/{branch}/"
        f"{relative_root}/workout.svg"
    )
    if notion_helper.heatmap_block_id:
        notion_helper.update_heatmap(
            block_id=notion_helper.heatmap_block_id,
            url=heatmap_url,
        )

notion_helper = NotionHelper()

if __name__ == "__main__":
    main()
