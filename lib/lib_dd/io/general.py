import numpy as np


def save_f(fid, final_iterations, norm_factors):
    """write model response directly in a file handler

    Also save forward response format to f_format.dat
    """
    for index, itd in enumerate(final_iterations):
        M = itd[0].Model.convert_to_M(itd[0].m)
        f_data = itd[0].Model.F(M)
        # we know that the first two dimensions belong to frequencies,
        # re/im
        base_dim = f_data.shape[0] * f_data.shape[1]

        if len(f_data.shape) == 3:
            extra_dim = f_data.shape[2]
        else:
            extra_dim = 1
        f_data = f_data.T

        # import pdb
        # pdb.set_trace()
        f_data = f_data.reshape(extra_dim, base_dim)
        if norm_factors is not None:
            print('normalising')
            f_data /= norm_factors[index]
        np.savetxt(fid, f_data)

    open('f_format.dat', 'w').write(itd[0].Data.obj.data_format)
