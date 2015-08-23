from __future__ import absolute_import

import numpy as np

from ._odeint_numpy import integrate_adaptive as _integrate_adaptive


def integrate_adaptive(f, j, ny, atol, rtol, y0, x0, xend, dx0,
                       check_callable=True, check_indexing=True):

    # Sanity checks to reduce risk of having a segfault:
    if check_callable:
        _fout = np.empty(ny)
        _ret = f(x0, y0, _fout)
        if _ret is not None:
            raise ValueError("f() must return None")

        _jmat_out = np.empty((ny, ny))
        _dfdx_out = np.empty(ny)
        _ret = j(x0, y0, _jmat_out, _dfdx_out)
        if _ret is not None:
            raise ValueError("j() must return None")

    if check_indexing:
        _fout_short = np.empty(ny-1)
        try:
            f(x0, y0, _fout_short)
        except IndexError:
            pass
        else:
            raise ValueError("All elements in fout not assigned in f()")

        _jmat_out_short = np.empty((ny, ny-1))
        try:
            j(x0, y0, _jmat_out_short, _dfdx_out)
        except IndexError:
            pass
        else:
            raise ValueError("All elements in Jout not assigned in j()")
        _dfdx_out_short = np.empty(ny-1)
        try:
            j(x0, y0, _jmat_out, _dfdx_out_short)
        except IndexError:
            pass
        else:
            raise ValueError("All elements in dfdx_out not assigned in j()")

    return _integrate_adaptive(f, j, ny, atol, rtol, y0, x0, xend, dx0)
