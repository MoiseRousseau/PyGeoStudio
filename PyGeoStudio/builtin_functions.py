import numpy as np

def VanGenuchtenWC(psi, tets, a, n, tetr):
  """
  Van Genuchten model for volumetric water content from `Van Genuchten (1980) <https://doi.org/10.2136/sssaj1980.03615995004400050002x>`_ as:
  
  .. math::

    \theta(\psi)=\theta_s \: \ln \left( e + (\frac{\psi}{a})^n \right) ^{-m}
  
  :param psi: Pressure head / water suction (m)
  :type psi: numpy array
  :param tets: Water content at saturation
  :type tets: float
  :param tetr: Residual water content
  :type tetr: float
  :param a: Van Genuchten a parameter (related to air entry value)
  :type a: float
  :param n: Van Genuchten n parameter (related to curve inflexion)
  :type n: float
  :return: Water content at the given suction
  :rtype: numpy array
  """
  return tetr+((tets-tetr)/(1+(((a*psi)**n)**(1-(1/n)))))


def VanGenuchtenMualemK(theta, n):
  """
  Van Genuchten - Mualem model for the relative hydraulic conductivity from `Van Genuchten (1980) <https://doi.org/10.2136/sssaj1980.03615995004400050002x>`_ as:
  
  .. math::

    \K_r(\theta)=\theta^(1/2) \: \left( 1 - ( 1 - \theta^(1/m) ) ^m \right) ^ 2
  
  where `:math: m=1-1/n`
  
  :param theta: Water content
  :type psi: numpy array
  :param n: Van Genuchten n parameter
  :type n: float
  :return: Relative hydraulic conductivity at the given water content
  :rtype: numpy array
  """
  m = 1 - 1/n
  return np.sqrt(theta) * ( 1 - (1-theta**(1/m))**m ) ** 2


def VanGenuchtenBurdineK(theta, n):
  """
  Van Genuchten - Burdine model for the relative hydraulic conductivity from `Van Genuchten (1980) <https://doi.org/10.2136/sssaj1980.03615995004400050002x>`_ as:
  
  .. math::

    \K_r(\theta)=\theta^2 \: \left( 1 - ( 1 - \theta^(1/m) ) ^m \right)
  
  where `:math: m=1-1/n`
  
  :param theta: Water content
  :type psi: numpy array
  :param n: Van Genuchten n parameter
  :type n: float
  :return: Relative hydraulic conductivity at the given water content
  :rtype: numpy array
  """
  m = 1 - 1/n
  return np.sqrt(theta) * ( 1 - (1-theta**(1/m))**m ) ** 2


def FredlundXingWC(psi, tets, a, n, m):
  """
  Fredlund and Xing model for volumetric water content from `Fredlund and Xing (1994) <https://doi.org/10.1139/t94-061>`_ as:
  
  .. math::

    \theta(\psi)=\theta_r+ \frac{\displaystyle \theta_s-\theta_r}{\displaystyle (1+(a \psi)^n)^{1-1/n}}
  
  :param psi: Pressure head / water suction (m)
  :type psi: numpy array
  :param tets: Water content at saturation
  :type tets: float
  :param a: Fredlund and Xing a parameter
  :type a: float
  :param n: Fredlund and Xing n parameter
  :type n: float
  :param m: Fredlund and Xing m parameter
  :type m: float
  :return: Water content at the given suction
  :rtype: numpy array
  """
  return tets * (np.log(np.e + (psi/a)**n))**(-m)
