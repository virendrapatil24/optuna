import tempfile

import optuna
import optuna.trial


def _create_some_study() -> optuna.Study:
    def f(trial: optuna.trial.Trial) -> float:

        x = trial.suggest_float("x", -10, 10)
        y = trial.suggest_float("y", 10, 20, log=True)
        z = trial.suggest_categorical("z", (10.0, 20.5, 30.0))
        assert isinstance(z, float)

        return x ** 2 + y ** 2 + z

    study = optuna.create_study()
    study.optimize(f, n_trials=100)
    return study


def test_write() -> None:

    study = _create_some_study()

    with tempfile.NamedTemporaryFile("r") as tf:
        optuna.dashboard._write(study, tf.name)

        html = tf.read()
        assert "<body>" in html
        assert "bokeh" in html
