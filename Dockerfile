FROM freqtradeorg/freqtrade:stable

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY user_data/strategies/ /freqtrade/user_data/strategies/
COPY strategy_selector.py /freqtrade/

USER ftuser
