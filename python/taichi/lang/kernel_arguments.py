from taichi.lang.core import taichi_lang_core
from taichi.lang.expr import Expr
from taichi.lang.util import cook_dtype, to_taichi_type


class ArgExtArray:
    def __init__(self, dim=1):
        assert dim == 1

    def extract(self, x):
        return to_taichi_type(x.dtype), len(x.shape)


ext_arr = ArgExtArray


class Template:
    def __init__(self, tensor=None, dim=None):
        self.tensor = tensor
        self.dim = dim

    def extract(self, x):
        import taichi as ti
        if isinstance(x, ti.SNode):
            return x.ptr
        if isinstance(x, ti.Expr):
            return x.ptr.get_underlying_ptr_address()
        if isinstance(x, ti.core.Expr):
            return x.get_underlying_ptr_address()
        if isinstance(x, tuple):
            return tuple(self.extract(item) for item in x)
        return x


template = Template


def decl_scalar_arg(dtype):
    dtype = cook_dtype(dtype)
    id = taichi_lang_core.decl_arg(dtype, False)
    return Expr(taichi_lang_core.make_arg_load_expr(id, dtype))


def decl_ext_arr_arg(dtype, dim):
    dtype = cook_dtype(dtype)
    id = taichi_lang_core.decl_arg(dtype, True)
    return Expr(taichi_lang_core.make_external_tensor_expr(dtype, dim, id))


def decl_scalar_ret(dtype):
    dtype = cook_dtype(dtype)
    id = taichi_lang_core.decl_ret(dtype)
    return id
