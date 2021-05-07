from pathlib import Path

import matplotlib.pyplot as plt


def setup_case_study(
    script_path, output_folder_name="pyglotaran_examples_output", results_folder_root=None
):
    script_folder = script_path.parent
    print(f"Executing: {script_path.name} from {script_folder}")
    if results_folder_root is None:
        results_folder_root = Path.home().joinpath(output_folder_name)
    results_folder_root.mkdir(exist_ok=True)
    script_folder_rel = script_folder.relative_to(script_folder.parent.parent)
    results_folder = results_folder_root.joinpath(script_folder_rel)
    print(f"Saving results in: {results_folder}")
    return results_folder, script_folder


def simple_plot_overview(res, title=None):
    """simple plotting function derived from code from pyglotaran_extras"""
    fig, ax = plt.subplots(2, 3, figsize=(12, 6), constrained_layout=True)
    if title:
        fig.suptitle(title, fontsize=16)
    sas = res.species_associated_spectra
    traces = res.species_concentration
    if "spectral" in traces.coords:
        traces.sel(spectral=res.spectral.values[0], method="nearest").plot.line(
            x="time", ax=ax[0, 0]
        )
    else:
        traces.plot.line(x="time", ax=ax[0, 0])
    sas.plot.line(x="spectral", ax=ax[0, 1])
    rLSV = res.residual_left_singular_vectors
    rLSV.isel(left_singular_value_index=range(min(2, len(rLSV)))).plot.line(x="time", ax=ax[1, 0])

    ax[1, 0].set_title("res. LSV")
    rRSV = res.residual_right_singular_vectors
    rRSV.isel(right_singular_value_index=range(min(2, len(rRSV)))).plot.line(
        x="spectral", ax=ax[1, 1]
    )

    ax[1, 1].set_title("res. RSV")
    res.data.plot(x="time", ax=ax[0, 2])
    ax[0, 2].set_title("data")
    res.residual.plot(x="time", ax=ax[1, 2])
    ax[1, 2].set_title("residual")
    plt.show(block=False)
    return fig
