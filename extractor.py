import os
from concurrent.futures import ThreadPoolExecutor

class Extractor:
    def __init__(self, logger):
        self.logger = logger

    def create_directory_structure(self, output_dir, parent_id):
        root_path = os.path.join(output_dir, "Root")
        parent_path = os.path.join(root_path, str(parent_id))
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        return parent_path

    def process_parent(self, file_path, output_dir, parent_id, children, anim_data_start):
        try:
            parent_dir = self.create_directory_structure(output_dir, parent_id)
            with open(file_path, "rb") as f:
                for index, (child_id, frame_count, logical_offset) in enumerate(children):
                    absolute_offset = anim_data_start + logical_offset
                    next_offset = (
                        children[index + 1][2] if index < len(children) - 1 else None
                    )
                    size = (
                        next_offset - logical_offset
                        if next_offset is not None
                        else os.path.getsize(file_path) - absolute_offset
                    )
                    if size <= 0:
                        self.logger.log_error(
                            "ERR_INVALID_SIZE",
                            f"Invalid size for child {child_id} of parent {parent_id}.",
                        )
                        continue

                    f.seek(absolute_offset)
                    data = f.read(size)

                    child_file_path = os.path.join(parent_dir, f"{child_id}.yka")
                    with open(child_file_path, "wb") as child_file:
                        child_file.write(data)

            self.logger.log_info(f"Parent ID {parent_id} processed successfully.")
        except Exception as e:
            self.logger.log_error(
                "ERR_PARENT_PROCESS", f"Failed to process Parent ID {parent_id}.", e
            )

    def extract_files(self, file_path, output_dir, toc_entries, anim_data_start):
        self.logger.log_info("Starting optimized file extraction process...")
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.process_parent, file_path, output_dir, parent_id, children, anim_data_start
                )
                for parent_id, children in toc_entries.items()
            ]
            for future in futures:
                future.result()  # Ensure all tasks complete

        self.logger.log_info("Optimized file extraction process completed.")
