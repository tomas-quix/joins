```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
mbr_forward[mbr_forward] -->|pre-join|join[join];
mbr_enc_forward[mbr_enc_forward] -->|pre-join|join[join];
mbr_replay[mbr_replay] -->|mbr|mbr_forward[mbr_forward];
mbr_enc_replay[mbr_enc_replay] -->|mbr_enc|mbr_enc_forward[mbr_enc_forward];

```