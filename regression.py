import warnings
warnings.filterwarnings('ignore')

# linear models: http://scikit-learn.org/stable/modules/linear_model.html#stochastic-gradient-descent-sgd
from sklearn.linear_model import \
    LinearRegression, Ridge, Lasso, ElasticNet, \
    Lars, LassoLars, \
    OrthogonalMatchingPursuit, \
    BayesianRidge, ARDRegression, \
    SGDRegressor, \
    PassiveAggressiveRegressor, \
    RANSACRegressor, HuberRegressor

from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import StandardScaler

# svm models: http://scikit-learn.org/stable/modules/svm.html
from sklearn.svm import SVR, NuSVR, LinearSVR

# neighbor models: http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.RadiusNeighborsRegressor.html#sklearn.neighbors.RadiusNeighborsRegressor
from sklearn.neighbors import RadiusNeighborsRegressor, KNeighborsRegressor

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, DotProduct, Matern, StationaryKernelMixin, WhiteKernel

from utilities import *
from universal_params import *


def gen_reg_data(x_mu=10., x_sigma=1., num_samples=100, num_features=3,
                 y_formula=sum, y_sigma=1.):
    """
    generate some fake data for us to work with
    :return: x, y
    """
    x = np.random.normal(x_mu, x_sigma, (num_samples, num_features))
    y = np.apply_along_axis(y_formula, 1, x) + np.random.normal(0, y_sigma, (num_samples,))

    return x, y


linear_models_n_params = [
    (LinearRegression, normalize),

    (Ridge,
     {**alpha, **normalize, **tol,
      'solver': ['svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']
      }),

    (Lasso,
     {**alpha, **normalize, **tol, **warm_start
      }),

    (ElasticNet,
     {**alpha, **normalize, **tol,
      'l1_ratio': [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9],
      }),

    (Lars,
     {**normalize,
      'n_nonzero_coefs': [100, 300, 500, np.inf],
      }),

    (LassoLars,
     {**normalize, **max_iter_inf, **normalize, **alpha
      }),

    (OrthogonalMatchingPursuit,
     {'n_nonzero_coefs': [100, 300, 500, np.inf, None],
      **tol, **normalize
      }),

    (BayesianRidge,
     {
         'n_iter': [100, 300, 1000],
         **tol, **normalize,
         'alpha_1': [1e-6, 1e-4, 1e-2, 0.1, 0],
         'alpha_2': [1e-6, 1e-4, 1e-2, 0.1, 0],
         'lambda_1': [1e-6, 1e-4, 1e-2, 0.1, 0],
         'lambda_2': [1e-6, 1e-4, 1e-2, 0.1, 0],
     }),

    # WARNING: ARDRegression takes a long time to run
    (ARDRegression,
     {'n_iter': [100, 300, 1000],
      **tol, **normalize,
      'alpha_1': [1e-6, 1e-4, 1e-2, 0.1, 0],
      'alpha_2': [1e-6, 1e-4, 1e-2, 0.1, 0],
      'lambda_1': [1e-6, 1e-4, 1e-2, 0.1, 0],
      'lambda_2': [1e-6, 1e-4, 1e-2, 0.1, 0],
      'threshold_lambda': [1e2, 1e3, 1e4, 1e6]}),

    (SGDRegressor,
     {'loss': ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
      **penalty_12e, **n_iter, **epsilon, **eta0,
      'alpha': [1e-6, 1e-5, 1e-2, 'optimal'],
      'l1_ratio': [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9],
      'learning_rate': ['constant', 'optimal', 'invscaling'],
      'power_t': [0.1, 0.25, 0.5]
      }),

    (PassiveAggressiveRegressor,
     {**C, **epsilon, **n_iter, **warm_start,
      'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive']
      }),

    (RANSACRegressor,
     {'min_samples': [0.1, 0.5, 0.9, None],
      'max_trials': n_iter['n_iter'],
      'stop_score': [0.8, 0.9, 1],
      'stop_probability': [0.9, 0.95, 0.99, 1],
      'loss': ['absolute_loss', 'squared_loss']
      }),

    (HuberRegressor,
     { 'epsilon': [1.1, 1.35, 1.5, 2],
       **max_iter, **alpha, **warm_start, **tol
       }),

    (KernelRidge,
     {**alpha, **degree, **gamma, **coef0
      })
]

svm_models_n_params_small = [
    (SVR,
     {**C_small, **epsilon, **kernel, **degree, **gamma_small, **coef0_small, **shrinking
      }),

    (NuSVR,
     {**C_small, **nu_small, **kernel, **degree, **gamma_small, **coef0_small, **shrinking,
      }),

    (LinearSVR,
     {**C_small, **epsilon,
      'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'],
      'intercept_scaling': [0.1, 1, 10]
      })
]

svm_models_n_params = [
    (SVR,
     {**C, **epsilon, **kernel, **degree, **gamma, **coef0, **shrinking, **tol, **max_iter_inf2
      }),

    (NuSVR,
     {**C, **nu, **kernel, **degree, **gamma, **coef0, **shrinking , **tol, **max_iter_inf2
     }),

    (LinearSVR,
     {**C, **epsilon, **tol, **max_iter,
      'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'],
      'intercept_scaling': [0.1, 0.5, 1, 5, 10]
      })
]

neighbor_models_n_params = [
    (RadiusNeighborsRegressor,
     {**neighbor_radius, **neighbor_algo, **neighbor_leaf_size, **neighbor_metric,
      'weights': ['uniform', 'distance'],
      'p': [1, 2],
     }),

    (KNeighborsRegressor,
     {**n_neighbors, **neighbor_algo, **neighbor_leaf_size, **neighbor_metric,
      'p': [1, 2],
      'weights': ['uniform', 'distance'],
      })
]


gaussianprocee_models_n_params = [
    (GaussianProcessRegressor,
     {'kernel': [RBF(), ConstantKernel(), DotProduct(), WhiteKernel()],
      'n_restarts_optimizer': [3],
      'alpha': [1e-10, 1e-5],
      'normalize_y': [True, False]
      })
]

x, y = gen_reg_data(10, 3, 100, 3, sum, 0.3)

big_loop(gaussianprocee_models_n_params,
         StandardScaler().fit_transform(x), y, isClassification=False)