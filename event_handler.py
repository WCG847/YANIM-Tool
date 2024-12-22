
class EventHandler:
    def __init__(self, tree, logger):
        self.tree = tree
        self.logger = logger

    def expand_all(self):
        self.logger.log_info("Expanding all tree nodes...")
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
        self.logger.log_info("All tree nodes expanded.")

    def collapse_all(self):
        self.logger.log_info("Collapsing all tree nodes...")
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
        self.logger.log_info("All tree nodes collapsed.")
