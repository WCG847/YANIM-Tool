from tkinter import ttk

class TreeViewManager:
    def __init__(self, parent, columns, logger):
        self.logger = logger
        self.tree = ttk.Treeview(parent, columns=columns, show="tree headings")
        self.tree.heading("#0", text="Parent/Child Relationship")
        for col in columns:
            self.tree.heading(col, text=col)

    def attach_scrollbar(self, parent):
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return scrollbar

    def populate(self, toc_entries):
        self.logger.log_info("Populating TreeView...")
        for parent_id, children in toc_entries.items():
            parent_node = self.tree.insert("", "end", text=f"Parent ID: {parent_id}")
            for child_id, frame_count, offset in children:
                self.tree.insert(
                    parent_node, "end", text=f"Child ID: {child_id}",
                    values=(frame_count, f"0x{offset:X}")
                )
        self.logger.log_info("TreeView populated successfully.")

    def clear(self):
        self.logger.log_info("Clearing TreeView...")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.logger.log_info("TreeView cleared.")

    def get_treeview(self):
        return self.tree
