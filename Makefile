KIND_CLUSTER_NAME := timekeeper
KUSTOMIZE_VERSION := v5.1.1
KIND_VERSION := v0.20.0

up:
	-make down
	time kind create cluster --name $(KIND_CLUSTER_NAME)

down:
	kind delete cluster --name $(KIND_CLUSTER_NAME)

up-if-down:
	# Check if cluster is running. Start it if not running.
	kind get clusters | grep $(KIND_CLUSTER_NAME) \
	  && kubectl cluster-info \
	  || make up

dev: up-if-down clean
	skaffold dev

download-kustomize:
	curl -o kustomize.tar.gz --location https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/$(KUSTOMIZE_VERSION)/kustomize_$(KUSTOMIZE_VERSION)_linux_amd64.tar.gz
	tar -xzvf kustomize.tar.gz kustomize
	rm kustomize.tar.gz
	chmod u+x ./kustomize

download-kind:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/$(KIND_VERSION)/kind-linux-amd64
	chmod +x ./kind

download-skaffold:
	curl -Lo ./skaffold https://storage.googleapis.com/skaffold/releases/v2.6.3/skaffold-linux-amd64
	chmod +x ./skaffold

install-deps-global: download-skaffold download-kustomize download-kind
	mv skaffold /usr/bin
	mv kustomize /usr/bin
	mv kind /usr/bin

install-deps-local: download-skaffold download-kustomize download-kind
	-mv skaffold ~/.local/bin
	-mv kustomize ~/.local/bin
	-mv kind ~/.local/bin

code-stats:
	tree
	# https://github.com/AlDanial/cloc
	cloc .

clean:
	@echo
