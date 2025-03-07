# global
import numpy as np
from hypothesis import assume, strategies as st, given

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import (
    handle_frontend_method,
    assert_all_close,
)
import ivy_tests.test_ivy.test_frontends.test_numpy.helpers as np_frontend_helpers
from ivy_tests.test_ivy.test_functional.test_core.test_linalg import (
    _get_first_matrix_and_dtype,
    _get_second_matrix_and_dtype,
)
import ivy_tests.test_ivy.helpers.test_parameter_flags as pf
from ivy.functional.frontends.numpy import ndarray


CLASS_TREE = "ivy.functional.frontends.numpy.ndarray"


@given(
    dtype_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        ret_shape=True,
    ),
)
def test_numpy_ndarray_property_ivy_array(
    dtype_x,
):
    dtype, data, shape = dtype_x
    x = ndarray(shape, dtype[0])
    x.ivy_array = data[0]
    ret = helpers.flatten_and_to_np(ret=x.ivy_array.data)
    ret_gt = helpers.flatten_and_to_np(ret=data[0])
    helpers.value_test(
        ret_np_flat=ret,
        ret_np_from_gt_flat=ret_gt,
        ground_truth_backend="numpy",
    )


@given(
    dtype_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        ret_shape=True,
    ),
)
def test_numpy_ndarray_property_dtype(
    dtype_x,
):
    dtype, data, shape = dtype_x
    x = ndarray(shape, dtype[0])
    x.ivy_array = data[0]
    ivy.assertions.check_equal(x.dtype, ivy.Dtype(dtype[0]))


@given(
    dtype_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        ret_shape=True,
    ),
)
def test_numpy_ndarray_property_shape(
    dtype_x,
):
    dtype, data, shape = dtype_x
    x = ndarray(shape, dtype[0])
    x.ivy_array = data[0]
    ivy.assertions.check_equal(x.shape, ivy.Shape(shape))


@given(
    dtype_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        ret_shape=True,
    ),
)
def test_numpy_ndarray_property_T(
    dtype_x,
):
    dtype, data, shape = dtype_x
    x = ndarray(shape, dtype[0])
    x.ivy_array = data[0]
    ret = helpers.flatten_and_to_np(ret=x.T.ivy_array)
    ret_gt = helpers.flatten_and_to_np(
        ret=ivy.permute_dims(ivy.native_array(data[0]), list(range(len(shape)))[::-1])
    )
    helpers.value_test(
        ret_np_flat=ret,
        ret_np_from_gt_flat=ret_gt,
        ground_truth_backend="numpy",
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="argmax",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        num_arrays=2,
    ),
)
def test_numpy_ndarray_argmax(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@st.composite
def dtypes_x_reshape(draw):
    dtypes, x = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("valid"),
            shape=helpers.get_shape(
                allow_none=False,
                min_num_dims=1,
                max_num_dims=5,
                min_dim_size=1,
                max_dim_size=10,
            ),
        )
    )
    shape = draw(helpers.reshape_shapes(shape=np.array(x).shape))
    return dtypes, x, shape


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="reshape",
    dtypes_x_shape=dtypes_x_reshape(),
    order=st.sampled_from(["C", "F", "A"]),
)
def test_numpy_ndarray_reshape(
    dtypes_x_shape,
    order,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, shape = dtypes_x_shape
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=[],
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "newshape": shape,
            "order": order,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="transpose",
    array_and_axes=np_frontend_helpers._array_and_axes_permute_helper(
        min_num_dims=2,
        max_num_dims=5,
        min_dim_size=2,
        max_dim_size=10,
    ),
)
def test_numpy_ndarray_transpose(
    array_and_axes,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    array, dtype, axes = array_and_axes
    helpers.test_frontend_method(
        init_input_dtypes=dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": np.array(array),
        },
        method_input_dtypes=dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axes": axes,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


# swapaxes
@st.composite
def dtype_values_and_axes(draw):
    dtype, x, x_shape = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("numeric"),
            min_num_dims=1,
            max_num_dims=5,
            ret_shape=True,
        )
    )
    axis1, axis2 = draw(
        helpers.get_axis(
            shape=x_shape,
            sorted=False,
            unique=True,
            min_size=2,
            max_size=2,
            force_tuple=True,
        )
    )
    return dtype, x, axis1, axis2


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="swapaxes",
    dtype_x_and_axes=dtype_values_and_axes(),
)
def test_numpy_ndarray_swapaxes(
    dtype_x_and_axes,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend,
    frontend_method_data,
):
    input_dtype, x, axis1, axis2 = dtype_x_and_axes
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_all_as_kwargs_np={
            "axis1": axis1,
            "axis2": axis2,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


# any
@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="any",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        valid_axis=True,
        force_int_axis=True,
        allow_neg_axes=True,
    ),
    keepdims=st.booleans(),
    where=np_frontend_helpers.where(),
)
def test_numpy_ndarray_any(
    dtype_x_axis,
    keepdims,
    where,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    where, as_variable, native_array = np_frontend_helpers.handle_where_and_array_bools(
        where=[where[0][0]] if isinstance(where, list) else where,
        input_dtype=input_dtype,
        as_variable=as_variable,
        native_array=native_array,
    )
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "out": None,
            "keepdims": keepdims,
            "where": where,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="all",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        valid_axis=True,
        force_int_axis=True,
        allow_neg_axes=True,
    ),
    keepdims=st.booleans(),
    where=np_frontend_helpers.where(),
)
def test_numpy_ndarray_all(
    dtype_x_axis,
    keepdims,
    where,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    where, as_variable, native_array = np_frontend_helpers.handle_where_and_array_bools(
        where=[where[0][0]] if isinstance(where, list) else where,
        input_dtype=input_dtype,
        as_variable=as_variable,
        native_array=native_array,
    )
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "out": None,
            "keepdims": keepdims,
            "where": where,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="argsort",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
)
def test_numpy_instance_argsort(
    dtype_x_axis,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        frontend=frontend,
        frontend_method_data=frontend_method_data,
        method_all_as_kwargs_np={
            "axis": axis,
            "kind": None,
            "order": None,
        },
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="mean",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("float"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
)
def test_numpy_ndarray_mean(
    dtype_x_axis,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_all_as_kwargs_np={
            "axis": axis,
            "dtype": "float64",
            "out": None,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="min",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
    keepdims=st.booleans(),
)
def test_numpy_instance_min(
    dtype_x_axis,
    keepdims,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "keepdims": keepdims,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="argmin",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=1,
        valid_axis=True,
        force_int_axis=True,
    ),
    keepdims=st.booleans(),
)
def test_numpy_ndarray_argmin(
    dtype_x_axis,
    keepdims,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_num_positional_args=method_num_positional_args,
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_all_as_kwargs_np={
            "axis": axis,
            "keepdims": keepdims,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="clip",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_num_dims=2,
    ),
)
def test_numpy_instance_clip(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_all_as_kwargs_np={"a_min": 0, "a_max": 1},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="max",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
    keepdims=st.booleans(),
)
def test_numpy_instance_max(
    dtype_x_axis,
    keepdims,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "keepdims": keepdims,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="cumprod",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
    dtype=helpers.get_dtypes("float", full=False, none=True),
)
def test_numpy_instance_cumprod(
    dtype_x_axis,
    dtype,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "dtype": dtype[0],
            "out": None,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="cumsum",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
    dtype=helpers.get_dtypes("float", full=False, none=True),
)
def test_numpy_instance_cumsum(
    dtype_x_axis,
    dtype,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
            "dtype": dtype[0],
            "out": None,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="diagonal",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_axis=0,
        max_axis=1,
        min_num_dims=1,
        force_int_axis=True,
    ),
)
def test_numpy_instance_diagonal(
    dtype_x_axis,
    axis1,
    axis2,
    offset,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis1, axis2 = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_num_positional_args=method_num_positional_args,
        method_native_array_flags=native_array,
        method_all_as_kwargs_np={
            "axis1": axis1,
            "axis2": axis2,
            "offset": offset,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="sort",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("float"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
)
def test_numpy_instance_sort(
    dtype_x_axis,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    ret, frontend_ret = helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
        test_values=False,
    )
    frontend_ret = np.sort(x[0], axis=axis)
    assert_all_close(
        ret_np=ret,
        ret_from_gt_np=frontend_ret,
        rtol=1e-2,
        atol=1e-2,
        ground_truth_backend="numpy",
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="copy",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_numpy_instance_copy(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="nonzero",
    dtype_and_a=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
    ),
)
def test_numpy_instance_nonzero(
    dtype_and_a,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, a = dtype_and_a

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": a[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="ravel",
    dtype_and_a=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
    ),
)
def test_numpy_instance_ravel(
    dtype_and_a,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, a = dtype_and_a

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": a[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="repeat",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=2,
        min_dim_size=2,
    ),
    repeats=helpers.ints(min_value=2, max_value=5),
    axis=helpers.ints(min_value=-1, max_value=1),
)
def test_numpy_instance_repeat(
    dtype_and_x,
    repeats,
    axis,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "repeats": repeats,
            "axis": axis,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="searchsorted",
    dtype_x_v=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("signed_integer"),
        min_num_dims=1,
        max_num_dims=1,
        num_arrays=2,
    ),
    side=st.sampled_from(["left", "right"]),
)
def test_numpy_instance_searchsorted(
    dtype_x_v,
    side,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_x_v

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "v": xs[1],
            "side": side,
            "sorter": np.argsort(xs[0]),
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="squeeze",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        force_int_axis=True,
    ),
)
def test_numpy_instance_squeeze(
    dtype_x_axis,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "axis": axis,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="std",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        max_value=100,
        valid_axis=True,
        force_int_axis=True,
    ),
    keepdims=st.booleans(),
    where=np_frontend_helpers.where(),
)
def test_numpy_instance_std(
    dtype_x_axis,
    keepdims,
    where,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    where, as_variable, native_array = np_frontend_helpers.handle_where_and_array_bools(
        where=[where[0][0]] if isinstance(where, list) else where,
        input_dtype=input_dtype,
        as_variable=as_variable,
        native_array=native_array,
    )
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "data": x[0],
        },
        method_all_as_kwargs_np={
            "axis": axis,
            "out": None,
            "ddof": 0,
            "keepdims": keepdims,
            "where": where,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__add__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"), num_arrays=2
    ),
)
def test_numpy_instance_add__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__sub__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"), num_arrays=2
    ),
)
def test_numpy_instance_sub__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__mul__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_mul__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__truediv__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_truediv__(
    dtype_and_x,
    as_variable,
    num_positional_args_method,
    native_array,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x
    assume(not np.any(np.isclose(xs[1], 0)))

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=1,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "data": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_num_positional_args=num_positional_args_method,
        method_native_array_flags=native_array,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend_method_data=frontend_method_data,
        frontend=frontend,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__pow__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
    ),
    power=helpers.ints(min_value=1, max_value=3),
)
def test_numpy_instance_pow__(
    dtype_and_x,
    power,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": power,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__and__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_and__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__or__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_or__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__xor__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_xor__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__matmul__",
    x=_get_first_matrix_and_dtype(),
    y=_get_second_matrix_and_dtype(),
)
def test_numpy_instance_matmul__(
    x,
    y,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    dtype1, x1 = x
    dtype2, x2 = y
    input_dtype = dtype1 + dtype2

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x1,
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": x2,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__copy__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_numpy_instance_copy__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__neg__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_numpy_instance_neg__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__pos__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_numpy_instance_pos__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__bool__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("integer"),
        max_dim_size=1,
    ),
)
def test_numpy_instance_bool__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__ne__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_ne__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__eq__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_eq__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__ge__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_ge__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__gt__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_gt__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__le__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_le__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__lt__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        num_arrays=2,
    ),
)
def test_numpy_instance_lt__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__int__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_dim_size=1,
        max_dim_size=1,
    ),
)
def test_numpy_instance_int__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__float__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_dim_size=1,
        max_dim_size=1,
    ),
)
def test_numpy_instance_float__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__contains__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
    ),
)
def test_numpy_instance_contains__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "key": xs[0].reshape(-1)[0],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__iadd__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"), num_arrays=2
    ),
)
def test_numpy_instance_iadd__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__isub__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"), num_arrays=2
    ),
)
def test_numpy_instance_isub__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__imul__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"), num_arrays=2
    ),
)
def test_numpy_instance_imul__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__ipow__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
    ),
    power=helpers.ints(min_value=1, max_value=3),
)
def test_numpy_instance_ipow__(
    dtype_and_x,
    power,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": power,
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__iand__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_iand__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__ior__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_ior__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__ixor__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("bool"),
        num_arrays=2,
    ),
)
def test_numpy_instance_ixor__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__imod__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        num_arrays=2,
        min_value=0,
        exclude_min=True,
    ),
)
def test_numpy_instance_imod__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    native_array: pf.NativeArrayFlags,
    init_num_positional_args: pf.NumPositionalArgFn,
    method_num_positional_args: pf.NumPositionalArgMethod,
    frontend_method_data,
    frontend,
):
    input_dtype, xs = dtype_and_x
    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        method_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=init_num_positional_args,
        init_native_array_flags=native_array,
        method_as_variable_flags=as_variable,
        method_native_array_flags=native_array,
        method_num_positional_args=method_num_positional_args,
        init_all_as_kwargs_np={
            "object": xs[0],
        },
        method_all_as_kwargs_np={
            "value": xs[1],
        },
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )


@handle_frontend_method(
    class_tree=CLASS_TREE,
    init_tree="numpy.array",
    method_name="__abs__",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_numpy_instance_abs__(
    dtype_and_x,
    as_variable: pf.AsVariableFlags,
    num_positional_args_method: pf.NumPositionalArgMethod,
    native_array: pf.NativeArrayFlags,
    frontend_method_data,
    frontend,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_method(
        init_input_dtypes=input_dtype,
        init_as_variable_flags=as_variable,
        init_num_positional_args=1,
        init_native_array_flags=native_array,
        init_all_as_kwargs_np={
            "data": x[0],
        },
        method_input_dtypes=input_dtype,
        method_as_variable_flags=as_variable,
        method_num_positional_args=num_positional_args_method,
        method_native_array_flags=native_array,
        method_all_as_kwargs_np={},
        frontend=frontend,
        frontend_method_data=frontend_method_data,
    )
