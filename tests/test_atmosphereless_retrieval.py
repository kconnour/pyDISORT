import numpy as np
import disort


def test_retrieval_without_atmosphere_gives_expected_result():
    # This test is not particularly well designed, but it ensures that the
    #  compiled .so file is working as expected.

    # Define computational parameters
    n_streams = 32
    n_polar = 1
    n_azimuth = 1

    # Define angles
    solar_zenith_angle = 45
    emission_angle = 55
    azimuth = 79.98657967235727
    mu0 = np.cos(np.radians(solar_zenith_angle))
    mu = np.cos(np.radians(emission_angle))

    # Define an empty atmosphere
    z = np.linspace(100000, 0, num=15)
    optical_depth = np.zeros((z.shape[0] - 1))
    ssa = np.ones((z.shape[0] - 1))
    pmom = np.zeros((128, z.shape[0]-1))
    pmom[0] = 1

    # Define output arrays
    n_user_levels = z.shape[0]
    albedo_medium = np.zeros((1,))
    diffuse_up_flux = np.zeros((15,))
    diffuse_down_flux = np.zeros((15,))
    direct_beam_flux = np.zeros((15,))
    flux_divergence = np.zeros((15,))
    intensity = np.zeros((1, 15, 1))
    mean_intensity = np.zeros((15,))
    transmissivity_medium = np.zeros((1,))

    # Define miscellaneous variables
    user_od_output = np.zeros(n_user_levels)
    temper = np.zeros(n_user_levels)
    h_lyr = np.zeros(n_user_levels)

    # Make the surface
    brdf_arg = np.array([1, 0.06, 0.7, 0.26, 0.3, 15])
    empty_bemst = np.zeros((16,))
    empty_emust = np.zeros((1,))
    empty_rho_accurate = np.zeros((1, 1))
    empty_rhou = np.zeros((n_streams, n_streams//2 + 1, n_streams))
    empty_rhoq = np.zeros((n_streams//2, n_streams//2 + 1, n_streams))

    rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(
        True, mu, np.pi, mu0, False, 0, False, empty_rhoq, empty_rhou, empty_emust,
        empty_bemst, False, azimuth, 0, empty_rho_accurate, 6, brdf_arg, 150,
        nstr=n_streams, numu=n_polar, nphi=n_azimuth)

    # Call DISORT
    rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed = \
        disort.disort(True, False, False, False, [False, False, False, False, False],
                      False, False, True, False,
                      optical_depth, ssa, pmom,
                      temper, 1, 1, user_od_output,
                      mu0, 0, mu, azimuth,
                      np.pi, 0, 0.1, 0, 0, 1, 3400000, h_lyr,
                      rhoq, rhou, rho_accurate, bemst, emust,
                      0, '', direct_beam_flux,
                      diffuse_down_flux, diffuse_up_flux, flux_divergence,
                      mean_intensity, intensity, albedo_medium,
                      transmissivity_medium, maxcmu=n_streams, maxulv=n_user_levels, maxmom=127)
    answer = uu[0, 0, 0]

    assert np.isclose(answer, 0.1695, atol=1e-3)
