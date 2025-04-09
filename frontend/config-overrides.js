module.exports = function override(config, env) {
    config.resolve = {
        fallback: {
            "wellknown": require.resolve("wellknown")
        }
    }
    return config;
}