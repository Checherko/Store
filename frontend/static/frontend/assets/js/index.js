var mix = {
        methods: {
                getBanners() {
                        try {
                                this.getData("/api/banners")
                                        .then(data => {
                                                this.banners = (Array.isArray(data) ? data : (data?.results || []))
                                                        .filter(b => b && typeof b === 'object')
                                                console.log('✅ Banners loaded:', this.banners.length)
                                        }).catch((e) => {
                                        this.banners = []
                                        console.warn('❌ Ошибка при получении баннеров:', e?.message)
                                })
                        } catch(e) { console.error('Banners error:', e) }
                },
                getPopularProducts() {
                        try {
                                this.getData("/api/products/popular")
                                        .then(data => {
                                                this.popularCards = (Array.isArray(data) ? data : (data?.results || []))
                                                        .filter(c => c && typeof c === 'object')
                                                console.log('✅ Popular products loaded:', this.popularCards.length, this.popularCards)
                                        })
                                        .catch((error) => {
                                                console.log('❌ Popular error:', error)
                                                this.popularCards = []
                                                console.warn('❌ Ошибка при получении списка популярных товаров')
                                        })
                        } catch(e) { console.error('Popular error:', e) }
                },
                getLimitedProducts() {
                        try {
                                this.getData("/api/products/limited")
                                        .then(data => {
                                                this.limitedCards = (Array.isArray(data) ? data : (data?.results || []))
                                                        .filter(c => c && typeof c === 'object')
                                                console.log('✅ Limited products loaded:', this.limitedCards.length)
                                        }).catch((e) => {
                                        this.limitedCards = []
                                        console.warn('❌ Ошибка при получении списка лимитированных товаров')
                                })
                        } catch(e) { console.error('Limited error:', e) }
                },
        },
        mounted() {
                console.log('🚀 Index.js mounted!')
                this.getBanners();
                this.getPopularProducts();
                this.getLimitedProducts();
        },
   created() {
     console.log('🚀 Index.js created!')
     this.getLimitedProducts()
   },
        data() {
                return {
                        banners: [],
                        popularCards: [],
                        limitedCards: [],
                }
        }
}