#!/usr/bin/env python3
"""Gera os artefatos visuais e o relatório auditável da entrega Cloud."""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EV = ROOT / "evidencias" / "reexecucao_2026-08-23" / "azure"
ICONS = ROOT / "evidencias" / "icones-azure-oficiais"
OUT = ROOT / "evidencias" / "entrega_final"
OUT.mkdir(parents=True, exist_ok=True)


def read(name: str) -> str:
    return (EV / name).read_text(encoding="utf-8")


def load(name: str):
    return json.loads(read(name))


def svg_data(name: str) -> str:
    raw = (ICONS / name).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


ICON = {
    "rg": "10007-icon-service-Resource-Groups.svg",
    "aci": "10104-icon-service-Container-Instances.svg",
    "acr": "10105-icon-service-Container-Registries.svg",
    "mysql": "10122-icon-service-Azure-Database-MySQL-Server.svg",
    "monitor": "00001-icon-service-Monitor.svg",
    "law": "00009-icon-service-Log-Analytics-Workspaces.svg",
    "appi": "00012-icon-service-Application-Insights.svg",
}


def architecture_svg() -> str:
    def image(key: str, x: int, y: int, size: int = 56) -> str:
        return f'<image href="{svg_data(ICON[key])}" x="{x}" y="{y}" width="{size}" height="{size}"/>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="930" viewBox="0 0 1600 930">
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#2563eb"/></marker><marker id="ao" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#7c3aed"/></marker><marker id="am" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#078760"/></marker><style>
.t{{font:700 27px Arial;fill:#102a43}}.h{{font:700 17px Arial;fill:#102a43}}.p{{font:14px Arial;fill:#334e68}}.n{{font:700 13px Arial;fill:#fff}}.box{{fill:#fff;stroke:#8db7df;stroke-width:2;rx:13}}.edge{{fill:none;stroke:#2563eb;stroke-width:3;marker-end:url(#a)}}.obs{{fill:none;stroke:#7c3aed;stroke-width:3;stroke-dasharray:9 7}}.obsarrow{{fill:none;stroke:#7c3aed;stroke-width:3;stroke-dasharray:9 7;marker-end:url(#ao)}}.metric{{fill:none;stroke:#078760;stroke-width:3;stroke-dasharray:3 7}}.metricarrow{{fill:none;stroke:#078760;stroke-width:3;stroke-dasharray:3 7;marker-end:url(#am)}}.lbl{{font:700 13px Arial;fill:#174ea6}}.olbl{{font:700 13px Arial;fill:#6d28d9}}.mlbl{{font:700 13px Arial;fill:#087654}}
</style></defs>
<rect width="1600" height="930" fill="#f5f9fd"/><text x="800" y="42" text-anchor="middle" class="t">Predictfy — Arquitetura Cloud executada na Sprint 3</text>
<rect x="340" y="82" width="1210" height="760" rx="20" fill="#eef6ff" stroke="#0078d4" stroke-width="4"/>{image('rg',365,95,42)}<text x="415" y="124" class="h">Resource Group rg-predictfy-sprint3-260823es</text>
<rect class="box" x="25" y="385" width="250" height="125"/><text x="150" y="423" text-anchor="middle" class="h">Usuários / cliente</text><text x="150" y="452" text-anchor="middle" class="p">horizonte + segmento</text><text x="150" y="480" text-anchor="middle" class="p">entrada da evidência</text>
<rect class="box" x="390" y="165" width="300" height="135"/>{image('acr',415,205)}<text x="495" y="203" class="h">Azure Container</text><text x="495" y="226" class="h">Registry</text><text x="495" y="256" class="p">Basic · privado</text><text x="495" y="280" class="p">2 imagens Docker :sprint3</text>
<rect class="box" x="790" y="165" width="310" height="135"/>{image('aci',815,205)}<text x="900" y="203" class="h">ACI — API FastAPI</text><text x="900" y="233" class="p">1 vCPU · 2 GB · porta 8000</text><text x="900" y="258" class="p">10 artefatos · health 200</text>
<rect class="box" x="790" y="385" width="310" height="165"/>{image('aci',815,430)}<text x="900" y="418" class="h">ACI — MySQL Bridge</text><text x="900" y="447" class="p">1 vCPU · 1,5 GB · porta 8080</text><text x="900" y="472" class="p">artefato de Machine Learning</text><text x="900" y="494" class="p">previsoes_baseline.json</text><text x="900" y="516" class="p">INSERT · SELECT · agregação</text><text x="900" y="538" class="p">OpenTelemetry</text>
<rect class="box" x="1200" y="385" width="300" height="165"/>{image('mysql',1225,430)}<text x="1310" y="423" class="h">Azure Database</text><text x="1310" y="446" class="h">for MySQL</text><text x="1310" y="478" class="p">Flexible Server · 8.0.21</text><text x="1310" y="503" class="p">B1ms · 32 GB · TLS</text><text x="1310" y="528" class="p">DB predictfy</text>
<rect class="box" x="390" y="650" width="300" height="130"/>{image('law',415,687)}<text x="500" y="687" class="h">Log Analytics</text><text x="500" y="717" class="p">ContainerInstanceLog_CL</text><text x="500" y="744" class="p">stdout · stderr · KQL</text>
<rect class="box" x="790" y="650" width="310" height="130"/>{image('appi',815,687)}<text x="900" y="687" class="h">Application Insights</text><text x="900" y="717" class="p">dependencies · exceptions</text><text x="900" y="744" class="p">customMetrics</text>
<rect class="box" x="1200" y="650" width="300" height="130"/>{image('monitor',1225,687)}<text x="1310" y="687" class="h">Azure Monitor</text><text x="1310" y="717" class="p">CPU · memória · SQL</text><text x="1310" y="744" class="p">métricas PT1M</text>
<path class="edge" d="M275 468 H790"/><text x="420" y="453" class="lbl">1 · horizonte + segmento</text>
<path class="edge" d="M690 232 H790"/><text x="708" y="216" class="lbl">pull API</text>
<path class="edge" d="M690 232 H740 V350 H945 V385"/><text x="755" y="336" class="lbl">pull bridge</text>
<path class="edge" d="M1100 468 H1200"/><text x="1115" y="452" class="lbl">2 · TLS / SQL</text>
<path class="obs" d="M1100 232 H1530 V590 H540"/><path class="obs" d="M945 550 V590"/><path class="obsarrow" d="M540 590 V650"/><text x="565" y="582" class="olbl">logs dos dois ACIs</text>
<path class="obsarrow" d="M945 590 V650"/><text x="960" y="625" class="olbl">OTel bridge</text>
<path class="obsarrow" d="M790 715 H690"/><text x="700" y="700" class="olbl">workspace-based</text>
<path class="metric" d="M1100 250 H1510 V620 H1350"/><path class="metric" d="M1100 510 H1170 V620"/><path class="metric" d="M1350 550 V620"/><path class="metricarrow" d="M1350 620 V650"/><text x="1180" y="612" class="mlbl">métricas: API · bridge · MySQL</text>
<text x="800" y="890" text-anchor="middle" class="p">Fluxo real documentado: cliente → bridge → artefato ML → MySQL; ACR alimenta os ACIs; Monitor, Log Analytics e Application Insights recebem sinais.</text></svg>'''


def drawio_xml() -> str:
    nodes = [
        ("acr","Azure Container Registry","Basic · 2 imagens Docker :sprint3",390,165,ICON["acr"]),
        ("api","ACI — API FastAPI","1 vCPU · 2 GB · :8000",790,165,ICON["aci"]),
        ("bridge","ACI — MySQL Bridge","previsoes_baseline.json · SQL · OTel",790,385,ICON["aci"]),
        ("mysql","Azure Database for MySQL","B1ms · 32 GB · TLS",1200,385,ICON["mysql"]),
        ("law","Log Analytics","logs centralizados · KQL",390,650,ICON["law"]),
        ("appi","Application Insights","OpenTelemetry · APM",790,650,ICON["appi"]),
        ("monitor","Azure Monitor","CPU · memória · SQL",1200,650,ICON["monitor"]),
    ]
    cells=[]
    for ident,title,sub,x,y,icon in nodes:
        uri=svg_data(icon).replace("&","&amp;")
        style=f"shape=label;image={uri};imageWidth=52;imageHeight=52;imageAlign=left;verticalAlign=middle;align=left;spacingLeft=76;spacingRight=12;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#8DB7DF;fontSize=14;"
        cells.append(f'<mxCell id="{ident}" value="&lt;b&gt;{title}&lt;/b&gt;&lt;br&gt;{sub}" style="{style}" vertex="1" parent="rg"><mxGeometry x="{x-340}" y="{y-80}" width="300" height="130" as="geometry"/></mxCell>')
    edges=[
        ("e1","acr","api","pull API","#2563EB","1","0.5","0","0.5","0"),
        ("e2","acr","bridge","pull bridge","#2563EB","1","0.5","0.5","0","0"),
        ("e3","bridge","mysql","TLS / SQL","#2563EB","1","0.5","0","0.5","0"),
        ("e4","api","law","logs","#7C3AED","1","0.5","0.5","0","1"),
        ("e5","bridge","law","logs","#7C3AED","0.5","1","0.5","0","1"),
        ("e6","bridge","appi","OpenTelemetry","#7C3AED","0.5","1","0.5","0","1"),
        ("e7","appi","law","workspace-based","#7C3AED","0","0.5","1","0.5","1"),
        ("e8","api","monitor","métricas","#078760","1","0.65","0.5","0","1"),
        ("e9","bridge","monitor","métricas","#078760","1","0.75","0.5","0","1"),
        ("e10","mysql","monitor","métricas","#078760","0.5","1","0.5","0","1"),
    ]
    for ident,src,dst,label,color,exit_x,exit_y,entry_x,entry_y,dashed in edges:
        cells.append(f'<mxCell id="{ident}" value="{label}" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;rounded=0;html=1;strokeWidth=2;endArrow=block;strokeColor={color};dashed={dashed};exitX={exit_x};exitY={exit_y};entryX={entry_x};entryY={entry_y};exitPerimeter=1;entryPerimeter=1;" edge="1" parent="rg" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    return f'''<mxfile host="app.diagrams.net" modified="2026-08-23T00:00:00.000Z" agent="Codex" version="24.7.17" type="device"><diagram id="predictfy-cloud-v2" name="Arquitetura Azure"><mxGraphModel dx="1600" dy="930" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="930"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="title" value="Predictfy AIOps — Arquitetura Cloud Sprint 3" style="text;html=1;align=center;fontSize=26;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="360" y="20" width="900" height="50" as="geometry"/></mxCell><mxCell id="rg" value="Microsoft Azure — Resource Group rg-predictfy-sprint3-260823es" style="swimlane;html=1;rounded=1;startSize=42;fillColor=#EEF6FF;strokeColor=#0078D4;strokeWidth=3;fontSize=16;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="340" y="80" width="1210" height="760" as="geometry"/></mxCell>{''.join(cells)}<mxCell id="user" value="&lt;b&gt;Cliente de evidência&lt;/b&gt;&lt;br&gt;horizonte + segmento" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#8DB7DF;fontSize=14;" vertex="1" parent="1"><mxGeometry x="25" y="385" width="250" height="125" as="geometry"/></mxCell><mxCell id="eu" value="1 · requisição" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;endArrow=block;strokeColor=#2563EB;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="user" target="bridge"><mxGeometry relative="1" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>'''


def metric_svg(filename: str, title: str) -> str:
    payload=load(filename); series=[]
    for metric in payload.get("value",[]):
        pts=[d.get("average") for d in metric.get("timeseries",[{}])[0].get("data",[]) if d.get("average") is not None]
        if pts: series.append((metric["name"]["localizedValue"],pts))
    colors=["#0078d4","#00a36c","#7c3aed","#e76f00","#c2185b"]
    chunks=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430"><rect width="1200" height="430" fill="#fff"/><text x="40" y="38" font-family="Arial" font-size="23" font-weight="700" fill="#102a43">{html.escape(title)}</text>']
    for idx,(name,pts) in enumerate(series):
        lo,hi=min(pts),max(pts); span=hi-lo or 1; x0=50; y0=85+idx*62; w=1100
        coords=" ".join(f"{x0+i*w/max(len(pts)-1,1):.1f},{y0+40-(v-lo)*38/span:.1f}" for i,v in enumerate(pts))
        chunks += [f'<text x="50" y="{y0-8}" font-family="Arial" font-size="14" fill="#334e68">{html.escape(name)} · min {lo:.2f} · máx {hi:.2f}</text>',f'<polyline points="{coords}" fill="none" stroke="{colors[idx%len(colors)]}" stroke-width="3"/>']
    chunks.append('<text x="50" y="410" font-family="Arial" font-size="13" fill="#627d98">Fonte: Azure Monitor API · intervalo PT1M · agregação Average · 23/08/2026 UTC</text></svg>')
    return "".join(chunks)


def codeblock(text: str) -> str:
    return f'<pre>{html.escape(text.strip())}</pre>'


def page(title: str, body: str) -> str:
    return f'<section class="page" style="border-top:0"><h1 style="border-left:5px solid #0078d4;padding-left:10px">{title}</h1>{body}<footer>Predictfy · FIAP 2TSCPW <span class="pageno"></span></footer></section>'


def shot(filename: str, caption: str) -> str:
    src = f"../reexecucao_2026-08-23/capturas_reais/{filename}"
    image_class = "shot portal-shot" if "portal_" in filename else "shot"
    return f'<figure><img class="{image_class}" src="{src}"><figcaption>{caption}</figcaption></figure>'


def report_html() -> str:
    resources=read("01_recursos.txt"); api=load("04_aci_api.json"); bridge=load("05_aci_bridge.json"); mysql=load("06_mysql.json"); logs=load("11_log_analytics_query.json")[:16]; appi=load("15_app_insights_telemetria.json")
    def render_log_rows(items):
        return "".join(f'<tr><td>{x["TimeGenerated"]}</td><td>{x["ContainerGroup_s"]}</td><td><code>{html.escape(x["Message"])}</code></td></tr>' for x in items)

    log_rows_1=render_log_rows(logs[:8])
    log_rows_2=render_log_rows(logs[8:])
    app_rows="".join(f'<tr><td>{r[0]}</td><td>{r[1]}</td></tr>' for r in appi["tables"][0]["rows"])
    body=[]
    body.append('<section class="page cover"><div><div class="eyebrow">Challenge Locaweb 2026 · Sprint 3</div><h1>Predictfy</h1><h2>Cloud Solutions &amp; Scalable Infrastructure</h2><p>Relatório técnico de arquitetura, infraestrutura como código, containers, Machine Learning, MySQL e observabilidade</p></div><footer>FIAP · 2TSCPW</footer></section>')
    body.append(page("Identificação e objetivo",'''<p><b>Nome do Grupo:</b> Predictfy</p><table><tr><th>Integrante</th><th>RM</th></tr><tr><td>Elton Vinicios Almeida de Oliveira</td><td>562187</td></tr><tr><td>Emerson dos Santos Silva</td><td>562033</td></tr><tr><td>Kelvin Douglas Ribeiro Rabelo</td><td>561538</td></tr><tr><td>Pedro Henrique Simão Soares</td><td>562283</td></tr><tr><td>Vitor Lucas Mattos de Brito Mariano</td><td>562116</td></tr></table><h2>Objetivo</h2><p>Transformar a lógica de AIOps da Predictfy em uma execução verificável no Microsoft Azure, com imagens privadas no ACR, dois containers no ACI, consumo de artefato de ML, persistência no Azure Database for MySQL e sinais no Azure Monitor, Log Analytics e Application Insights.</p>'''))
    body.append(page("Arquitetura da solução",'<img class="full" src="arquitetura_predictfy_azure.svg"><p class="caption">Figura 1 — arquitetura executada. Ícones do pacote oficial Azure Public Service Icons V24, Microsoft Architecture Center.</p>'))
    body.append(page("Fluxo e decisões de arquitetura",'''<ol><li>O ACR recebe builds remotos das imagens <code>predictfy-api:sprint3</code> e <code>predictfy-mysql-bridge:sprint3</code>.</li><li>O ACI da API comprova a execução da FastAPI e a presença dos dez conjuntos de artefatos analíticos.</li><li>O cliente de evidência envia horizonte e segmento ao bridge.</li><li>O bridge lê <code>previsoes_baseline.json</code>, calcula a saída, persiste sua proveniência no MySQL e expõe consulta e agregação.</li><li>Os ACIs enviam logs ao Log Analytics; o bridge envia OpenTelemetry ao Application Insights; Azure Monitor fornece métricas dos recursos.</li></ol><div class="callout"><b>Virtual Network:</b> não aplicada no MVP acadêmico. O enunciado a exige apenas “se aplicável”. A implantação efêmera usou endpoints públicos controlados; a evolução produtiva recomendada usa VNet, Private Endpoint, Key Vault e HTTPS gerenciado.</div>'''))
    body.append(page("Componentes e dimensionamento",'''<table><tr><th>Serviço</th><th>Configuração executada</th><th>Justificativa</th></tr><tr><td>Resource Group</td><td>rg-predictfy-sprint3-260823es</td><td>governança e descarte atômico</td></tr><tr><td>ACR</td><td>Basic, admin temporariamente habilitado</td><td>registro privado e build remoto</td></tr><tr><td>ACI API</td><td>1 vCPU, 2 GB, :8000</td><td>API e artefatos atuais</td></tr><tr><td>ACI Bridge</td><td>1 vCPU, 1,5 GB, :8080</td><td>integração ML–MySQL isolada</td></tr><tr><td>MySQL</td><td>B1ms, 32 GB, backup 1 dia</td><td>menor SKU acadêmico funcional</td></tr><tr><td>Log Analytics</td><td>30 dias</td><td>consulta KQL de stdout/stderr</td></tr><tr><td>Application Insights</td><td>workspace-based</td><td>APM via OpenTelemetry</td></tr></table>'''+shot("08_portal_resource_group.png","Figura 2 — visão consolidada do Resource Group no Portal. A lista comprova a criação conjunta do ACR, dos dois ACIs, do MySQL, do Log Analytics, do Application Insights e dos recursos automáticos de detecção.")))
    body.append(page("Preparação e configuração segura",'''<p>O provisionamento parte do <code>config.example.env</code>. Valores sensíveis são fornecidos somente no ambiente do shell e injetados como <code>secure-environment-variables</code>.</p>'''+codeblock("cp iac/config.example.env iac/config.env\n# editar nomes e segredos localmente; não versionar\nset -a\nsource iac/config.env\nset +a\naz login\naz account show --output table")+'''<div class="warning">Senha MySQL, chaves de API, connection strings, credenciais do ACR e tokens Entra foram omitidos das evidências.</div>'''))
    body.append(page("Provisionamento com Azure CLI",codeblock("bash 'Sprint 3/01_cloud/iac/01_provision.sh'")+'''<p>O script valida todas as variáveis, cria o Resource Group, Log Analytics, Application Insights, ACR, MySQL e banco. Tags <code>Project</code>, <code>Sprint</code>, <code>Discipline</code> e <code>Environment</code> permitem rastrear finalidade e custo.</p>'''+codeblock(resources)+shot("01_recursos_azure_terminal.png","Figura 3 — inventário obtido pela Azure CLI após o provisionamento. Os nomes, tipos e regiões confirmam que os serviços definidos na arquitetura foram materializados na assinatura.")))
    body.append(page("IaC do banco e restrição regional",'''<p>O arquivo <code>mysql_ephemeral.bicep</code> declara MySQL 8.0.21, tier Burstable, SKU Standard_B1ms, 32 GB, backup de um dia, sem HA e sem geobackup. A região Chile Central foi necessária porque a assinatura Azure for Students devolveu <code>ProvisionNotSupportedForRegion</code> nas demais regiões testadas.</p>'''+codeblock("az mysql flexible-server show -g $AZ_RESOURCE_GROUP -n $AZ_MYSQL_SERVER --query '{Estado:state,Versao:version,SKU:sku.name,Retencao:backup.backupRetentionDays}' -o json\n\n"+json.dumps(mysql,ensure_ascii=False,indent=2))+shot("04_mysql_terminal.png","Figura 7 — conferência pela CLI do servidor em estado Ready, banco predictfy e regra necessária para a comunicação dos serviços Azure durante a demonstração.")+shot("10_portal_mysql.png","Figura 7.1 — visão do MySQL Flexible Server no Portal, confirmando disponibilidade, versão, região e configuração do recurso provisionado.")))
    body.append(page("Build remoto e registro privado",codeblock("az acr build --registry $AZ_ACR_NAME --image predictfy-api:sprint3 --file locaweb/api/Dockerfile locaweb\naz acr build --registry $AZ_ACR_NAME --image predictfy-mysql-bridge:sprint3 --file 'Sprint 3/01_cloud/app_mysql/Dockerfile' .\naz acr repository show-tags -n $AZ_ACR_NAME --repository predictfy-api -o json\naz acr repository show-tags -n $AZ_ACR_NAME --repository predictfy-mysql-bridge -o json\n\n[\"sprint3\"]\n[\"sprint3\"]")+'''<p>O ACR fez os builds sem exigir Docker local. As imagens foram mantidas privadas, versionadas e consumidas pelos ACIs.</p>'''+shot("02_acr_builds_imagens_terminal.png","Figura 4 — os runs ch1 e ch2 aparecem como Succeeded. A consulta dos repositórios confirma a publicação das duas imagens Docker com a tag sprint3 no registro privado.")))
    body.append(page("Azure Container Instances",codeblock("az container show -g $AZ_RESOURCE_GROUP -n $AZ_CONTAINER_NAME --query '{Nome:name,Estado:instanceView.state,FQDN:ipAddress.fqdn,Imagem:containers[0].image}' -o json\n\nAPI:\n"+json.dumps(api,ensure_ascii=False,indent=2)+"\n\nBRIDGE:\n"+json.dumps(bridge,ensure_ascii=False,indent=2))+shot("03_aci_health_terminal.png","Figura 5 — API e bridge em estado Running, com suas imagens, FQDNs e dimensionamentos. Os dois health checks retornam HTTP 200; a API lista os artefatos analíticos e o bridge confirma banco e artefato disponíveis.")+shot("09_portal_aci_api.png","Figura 6 — visão operacional do ACI da API no Portal. O estado Running e o endereço público confirmam que a imagem privada foi iniciada pela infraestrutura Azure.")))
    body.append(page("Aplicação FastAPI em execução",codeblock("az container logs -g $AZ_RESOURCE_GROUP -n aci-predictfy-api\n\n"+read("09_api_logs.txt"))+'''<p>O health check retornou HTTP 200 e o startup listou dez conjuntos de artefatos: previsões de volume, LSTM, baseline, horizonte Prophet, risco OLA, clusters, KPI, comparação de modelos e segmentos.</p><p class="caption">Evidência 4 — stdout real do ACI API.</p>'''))
    body.append(page("Bridge: lógica ML e persistência",'''<p>O bridge é uma FastAPI mínima criada para demonstrar, sem alterar o MVP online, o consumo de um resultado real de ML e sua persistência. O artefato é lido em modo somente leitura e recebe SHA-256 para proveniência.</p>'''+codeblock("POST /executions/capture\n  1. valida X-Bridge-Key\n  2. lê previsoes_baseline.json\n  3. extrai segmento total e horizonte D+1\n  4. gera correlation_id e SHA-256\n  5. executa INSERT e COMMIT\n\nResultado registrado: baseline_sazonal_7d · D+1 · total · 44,0")+'''<div class="callout">Não são persistidos prompts, tokens Entra, chaves OpenAI ou dados pessoais.</div>'''))
    body.append(page("Schema MySQL",codeblock((ROOT/"app_mysql/schema.sql").read_text())+'''<p>A chave única de correlação impede duplicidade; o índice por modelo/data suporta auditoria; o <code>CHECK</code> impede valores negativos. O charset <code>utf8mb4</code> mantém compatibilidade textual.</p>'''))
    body.append(page("Inserção, consulta e processamento",codeblock("bash 'Sprint 3/01_cloud/iac/05_exercise_mysql.sh'\n\n[1/4] GET /health                         → 200 OK\n[2/4] POST /executions/capture            → 200 OK [INSERT]\n[3/4] GET /executions?limit=10             → 200 OK [SELECT]\n[4/4] GET /executions/summary              → 200 OK [COUNT + AVG + GROUP BY]\n\nmodelo=baseline_sazonal_7d | horizonte=D+1 | segmento=total\nmedia_prevista=44.00")+shot("05_ml_mysql_crud_terminal.png","Figura 8 — execução ponta a ponta: o bridge lê o baseline D+1, grava a previsão 44,0 com hash e correlation_id, recupera o registro por SELECT e calcula quantidade e média por GROUP BY.")))
    body.append(page("Logs do container bridge",codeblock("az container logs -g $AZ_RESOURCE_GROUP -n aci-predictfy-mysql-bridge\n\n"+read("10_bridge_logs.txt"))+'''<p>Os 200 confirmam health, inserção, consulta e agregação. O 401 comprova rejeição controlada de chamada sem chave. Os 404 são sondagens externas e não indicam falha dos endpoints documentados.</p>'''))
    body.append(page("Log Analytics e consulta KQL",codeblock("ContainerInstanceLog_CL\n| where TimeGenerated > ago(1h)\n| project TimeGenerated, ContainerGroup_s, Message\n| order by TimeGenerated desc")+f'''<table class="dense"><tr><th>UTC</th><th>Container</th><th>Mensagem</th></tr>{log_rows_1}</table>'''+shot("06_log_analytics_kql_terminal.png","Figura 9 — resultado real da consulta KQL. As linhas identificam o container de origem e registram health checks, captura, consulta e agregação, incluindo respostas 200 e a rejeição 401 sem credencial.")))
    body.append(page("Log Analytics — continuação",f'''<p>Continuação do resultado, incluindo inicialização da API e do bridge.</p><table class="dense"><tr><th>UTC</th><th>Container</th><th>Mensagem</th></tr>{log_rows_2}</table><p class="caption">Evidência 5B — total de 16 registros reais, sem linhas simuladas.</p>'''))
    body.append(page("Azure Monitor — ACI API",'<img class="full" src="metricas_aci_api.svg"><p>As séries contêm amostras reais após o início do container. Pontos anteriores sem valor foram omitidos do gráfico, sem interpolação.</p>'))
    body.append(page("Azure Monitor — ACI Bridge",'<img class="full" src="metricas_aci_bridge.svg"><p>O bridge apresentou atividade coerente com a janela de health, captura, listagem e agregação.</p>'))
    body.append(page("Azure Monitor — MySQL",'<img class="full" src="metricas_mysql.svg"><p>Foram coletados CPU, memória, conexões ativas, INSERT e SELECT. As séries foram preservadas integralmente em JSON.</p>'))
    body.append(page("Application Insights",codeblock("union withsource=Tabela requests, dependencies, exceptions, customMetrics\n| where timestamp > ago(1h)\n| summarize Registros=count() by Tabela\n| order by Tabela asc")+f'''<table><tr><th>Tabela</th><th>Registros</th></tr>{app_rows}</table><p>O recebimento de <code>dependencies</code>, <code>exceptions</code> e <code>customMetrics</code> comprova instrumentação efetiva por OpenTelemetry — não apenas a criação do recurso.</p>'''+shot("07_application_insights_terminal.png","Figura 10 — consulta da telemetria enviada pelo bridge. A presença de customMetrics, dependencies e exceptions demonstra tráfego efetivo pelo pipeline OpenTelemetry.")+shot("11_portal_application_insights.png","Figura 11 — visão do Application Insights no Portal, associado ao Log Analytics utilizado pela solução e preparado para centralizar a análise de desempenho da aplicação.")))
    body.append(page("Custos e encerramento",codeblock(read("16_descarte_azure.txt"))+'''<p>O ACR Basic, os ACIs mínimos e o MySQL B1ms reduziram custo. Após a coleta, <code>99_destroy.sh</code> validou o padrão seguro do Resource Group, exigiu o marcador de evidências e removeu o grupo integralmente. Os JSONs, logs e capturas preservam a comprovação da execução de 23/08/2026.</p><p class="caption"><b>Referências:</b> enunciado Locaweb — Sprint 3 Cloud, páginas 33–35; Microsoft Learn — Architecture Icons, ACR, ACI, Azure Database for MySQL, Azure Monitor, Log Analytics e Application Insights; Microsoft Azure Public Service Icons V24.</p>'''))
    css='''@page{size:A4 portrait;margin:12mm 0}*{box-sizing:border-box}body{margin:0;background:#dce6ef;color:#102a43;font:14px/1.45 Arial,sans-serif}.page{width:210mm;margin:5mm auto;padding:8mm 17mm;background:#fff;position:relative;break-inside:auto;page-break-inside:auto}.page:not(.cover)+.page:not(.cover){border-top:1px solid #d5e1ec}.cover{height:273mm;margin:0 auto;padding:17mm;background:linear-gradient(145deg,#061a3a,#075985 62%,#00a4ef);color:#fff;display:flex;align-items:center;page-break-after:always;break-after:page}.cover h1{font-size:46px;color:#fff;margin:10px 0}.cover h2{font-size:27px;color:#bde8ff}.cover p{font-size:19px;max-width:155mm}.eyebrow{text-transform:uppercase;letter-spacing:1.7px;color:#0078d4;font-weight:700;font-size:11px}.cover .eyebrow{color:#9bdeff}h1{font-size:25px;line-height:1.12;color:#082f57;margin:6px 0 12px}h2{font-size:18px;color:#075985;margin:14px 0 7px}h1,h2,pre,table,figure{break-inside:avoid;page-break-inside:avoid}h1,h2{break-after:avoid;page-break-after:avoid}p,li{font-size:13px}li{margin-bottom:5px}table{width:100%;border-collapse:collapse;margin:9px 0;font-size:11.5px}th{background:#075985;color:#fff;text-align:left}th,td{border:1px solid #bfd0df;padding:6px;vertical-align:top}.dense{font-size:8.5px}.dense th,.dense td{padding:3px}code{font-family:Menlo,monospace;font-size:.9em}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#071525;color:#c8f7d4;border-radius:8px;padding:10px;font:9.5px/1.42 Menlo,monospace;margin:8px 0}.callout,.warning,.pending{padding:9px 11px;border-left:5px solid #0078d4;background:#eaf6ff;margin:9px 0}.warning{border-color:#e76f00;background:#fff4df}.pending{border-color:#d97706;background:#fff7d6;font-size:11px}.full{display:block;max-width:100%;max-height:205mm;margin:8px auto}.caption{font-size:10px;color:#627d98}figure{margin:10px 0 4px}figcaption{font-size:10px;color:#627d98;margin-top:4px}.shot{display:block;width:100%;max-height:175mm;object-fit:contain;object-position:left top;border:1px solid #c9d8e5;border-radius:6px;background:#06111f}.portal-shot{width:84%;margin-left:auto;margin-right:auto}.stamp{display:inline-block;margin-top:20px;padding:8px 12px;border:1px solid #8edaff;border-radius:5px;font-weight:700}.ok{color:#087443;font-weight:700}.warn{color:#b45309;font-weight:700}footer{display:none}@media print{body{background:#fff}.page{margin:0 auto}.cover{margin:-12mm auto 0}}'''
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Locaweb Sprint 3 — Predictfy Cloud</title><style>'+css+'</style></head><body>'+''.join(body)+'</body></html>'


def main() -> None:
    (OUT/"arquitetura_predictfy_azure.svg").write_text(architecture_svg(),encoding="utf-8")
    drawio = drawio_xml().replace("Predictfy AIOps — Arquitetura Cloud Sprint 3", "Predictfy — Arquitetura Cloud Sprint 3")
    (ROOT/"arquitetura_predictfy_azure.drawio").write_text(drawio,encoding="utf-8")
    (OUT/"metricas_aci_api.svg").write_text(metric_svg("12_metricas_aci_api.json","Azure Monitor — ACI API"),encoding="utf-8")
    (OUT/"metricas_aci_bridge.svg").write_text(metric_svg("13_metricas_aci_bridge.json","Azure Monitor — ACI MySQL Bridge"),encoding="utf-8")
    (OUT/"metricas_mysql.svg").write_text(metric_svg("14_metricas_mysql.json","Azure Monitor — MySQL Flexible Server"),encoding="utf-8")
    (OUT/"RELATORIO_ENTREGA_COMPLETO.html").write_text(report_html(),encoding="utf-8")
    print(f"Artefatos gerados em {OUT}")


if __name__ == "__main__":
    main()
