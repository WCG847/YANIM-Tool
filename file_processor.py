
import os
import struct
from tkinter import messagebox

class FileProcessor:
    def __init__(self, logger, ce_key):
        self.logger = logger
        self.ce_key = ce_key
        self.toc_entries = {}
        self.anim_data_start = 0

    def load_file(self, file_path):
        self.logger.log_info(f"Loading file: {file_path}")
        if not os.path.exists(file_path):
            self.logger.log_error("ERR_FILE_NOT_FOUND", f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                self.logger.log_info("Reading TOC count...")
                f.seek(self.ce_key.YTOC_COUNT_OFFSET)
                toc_count_data = f.read(4)
                if len(toc_count_data) < 4:
                    raise ValueError("File is missing TOC count data.")
                toc_count = struct.unpack('<I', toc_count_data)[0]
                self.logger.log_info(f"TOC Count: {toc_count}")

                self.anim_data_start = self.ce_key.YTOC_OFFSET + (toc_count * 16)
                self.logger.log_info(f"AnimData Start: {self.anim_data_start}")

                # Read TOC Entries
                self.logger.log_info("Reading TOC entries...")
                f.seek(self.ce_key.YTOC_OFFSET)
                for i in range(toc_count):
                    entry_data = f.read(16)
                    if len(entry_data) < 16:
                        raise ValueError("File is missing TOC entry data.")

                    # Parse TOC entry (little-endian)
                    full_id = struct.unpack('<I', entry_data[:4])[0]
                    logical_offset = struct.unpack('<I', entry_data[4:8])[0]
                    frame_count = struct.unpack('<I', entry_data[8:12])[0]

                    child_id = full_id & 0xFFFF
                    parent_id = (full_id >> 16) & 0xFFFF
                    absolute_offset = self.anim_data_start + logical_offset

                    if parent_id not in self.toc_entries:
                        self.toc_entries[parent_id] = []
                    self.toc_entries[parent_id].append((child_id, frame_count, logical_offset))

                # Sort children by logical offset
                self.logger.log_info("Sorting children by logical offset...")
                for parent_id, children in self.toc_entries.items():
                    self.toc_entries[parent_id] = sorted(children, key=lambda x: x[2])

                self.logger.log_info("File loaded and TOC data successfully processed.")
                return self.toc_entries, self.anim_data_start

        except Exception as e:
            self.logger.log_error("ERR_LOAD_FILE", "Failed to load file.", e)
            raise
