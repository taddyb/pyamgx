cdef class Resources:
    """
    Resources: Class for creating and freeing AMGX Resources objects.
    """
    cdef AMGX_resources_handle rsrc

    def create_simple(self, Config cfg):
        """
        rsc.create_simple(cfg)

        Create the underlying AMGX Resources object in a
        single-threaded application.

        Parameters
        ----------
        cfg : Config

        Returns
        -------
        self : Resources
        """
        check_error(AMGX_resources_create_simple(&self.rsrc, cfg.cfg))
        return self

    def create(self, Config cfg, devices, mpi=False):
        """
        rsc.create(cfg, NULL, 1, devices)
        
        Create the underlying AMGX Resources object for a specific 
        device on a single-threaded application

        NOTE: the master node for MPI is 0

        Parameters
        ----------
        cfg : Config
        device : array_like

        Returns
        -------
        self : Resources
        """
        cdef int* nvamg_comm = NULL
        if mpi:
            MPI_Init(NULL, NULL)
            cdef int* master_node = 0  #
            nvamg_comm = NULL
        cdef int device_num = len(devices)
        cdef uintptr_t devices_ptr = ptr_from_array_interface(devices, "int32")
        check_error(AMGX_resources_create(&self.rsrc, cfg.cfg, nvamg_comm, device_num, <const int*> devices_ptr))
        return self

    def destroy(self):
        """
        rsc.destroy()

        Destroy the underlying AMGX Resources object.
        """
        check_error(AMGX_resources_destroy(self.rsrc))
