# -*- coding: utf-8 -*-
# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/precise64"
    config.vm.network :private_network, ip: "192.168.111.222"

    config.vm.define "local", primary: true  do |local|
        local.vm.network :forwarded_port, guest: 80, host: 8080
        local.vm.network :forwarded_port, guest: 8000, host: 8000
        local.vm.network :forwarded_port, guest: 3306, host: 3306
        local.vm.network :forwarded_port, guest: 11211, host: 11211

        local.vm.provision :ansible do |ansible|
            ansible.playbook = "playbooks/main.yml"
            ansible.inventory_path = "hosts"
            ansible.limit = 'all'
        end
    end

end
