import os

class CtrlImport:
    def __init__(self, tree, genv):
        self.get_basename = lambda filename: os.path.basename(filename).split('.', 1)[0]
        self.tree = tree
        path = self.tree[1]
        import_file = f"{path.replace('..', '../').replace('.', '/')}.txt"
        import_path = genv.get('IMPORT_PATH')
        import_path = '' if import_path == None else import_path
        import_file = os.path.join(import_path, import_file)
        import_path = os.path.dirname(import_file)
        genv['IMPORT_PATH'] = import_path
        self.import_file = import_file
        self.import_path = import_path
        self.cache_path = os.path.join(self.import_path, '__cache__')
        self.import_obj = os.path.join(self.cache_path, f'{self.get_basename(self.import_file)}.obj')
        print(path)
        print(import_file)
    def get_import_file(self):
        return self.import_file
    def is_update(self):
        if(self._cmp_file_time_stamp(self.import_file, self.import_obj) in [0, 1]):
            return False
        return True
    def create_cache(self, ast_tree):
        self._mkdir(self.cache_path)
        with open(self.import_obj, 'w', encoding='utf-8') as f:
            f.write(ast_tree)
    def get_ast_tree(self):
        with open(self.import_obj, encoding='utf-8') as f:
            ast_tree = f.read()
        return ast_tree
    def _mkdir(self, path):
        import os
        os.makedirs(path, exist_ok=True)
    def _zip(self):
        pass
    def _unzip(self):
        pass
    def _cmp_file_time_stamp(self, src, dst):
        if not os.path.exists(src):
            return -1
        if not os.path.exists(dst):
            return -2
        if os.path.getmtime(src) == os.path.getmtime(dst):
            return 0
        if os.path.getmtime(src) < os.path.getmtime(dst):
            return 1
        return 2
