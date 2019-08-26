kubectl create secret generic gregdb-wallet \
--from-file=./tns/cwallet.sso \
--from-file=./tns/ewallet.p12 \
--from-file=./tns/keystore.jks \
--from-file=./tns/ojdbc.properties \
--from-file=./tns/sqlnet.ora \
--from-file=./tns/tnsnames.ora \
--from-file=./tns/truststore.jks

kubectl create secret generic gregdb-admin-credentials \
--from-literal=username=ADMIN \
--from-literal=password=xxxxxx

kubectl create configmap webora-parameters \
--from-literal dbservice=db_high


kubectl create secret docker-registry ocirsecret \
--docker-server=<region-code>.ocir.io \
--docker-username='<tenancy-namespace>/<oci-username>' \
--docker-password='<oci-auth-token>' \
--docker-email='<email-address>'
