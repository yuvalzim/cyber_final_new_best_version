import process_check
import enable_py_privs

enable_py_privs.enable_privs()
process_check.close_proc(14528)